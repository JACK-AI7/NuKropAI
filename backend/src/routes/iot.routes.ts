import { FastifyInstance } from 'fastify';
import { IoTGateway } from '../iot/Gateway';
import { pool } from '../config/db';

const gateway = new IoTGateway();

// Start the gateway immediately to bind to MQTT/Tuya providers
gateway.start().catch(console.error);

export default async function iotRoutes(fastify: FastifyInstance) {
    
    // 1. WebSocket Endpoint for Real-time App Telemetry
    fastify.get('/telemetry/stream', { websocket: true }, (connection, req) => {
        const query = req.query as { deviceId?: string };
        fastify.log.info(`[WebSocket] Client connected for device: ${query.deviceId || 'ALL'}`);
        
        connection.socket.send(JSON.stringify({ event: 'connected', message: 'NuKrop IoT Stream Active' }));
        
        connection.socket.on('message', message => {
            // Mobile app can optionally send simple commands via WS too
            console.log('Received WebSocket message:', message.toString());
        });

        // In a real implementation, we would register this socket with the `IoTGateway`
        // so `broadcastWebSocketUpdate` sends data specifically to this socket.
    });

    // 2. Add / Bind New Device
    fastify.post('/devices/bind', async (request, reply) => {
        const { provider, providerDeviceId, credentials } = request.body as any;
        
        // Save to DB
        const client = await pool.connect();
        try {
            await client.query('BEGIN');
            // Assuming farmer_id is passed or extracted from JWT
            const res = await client.query(
                `INSERT INTO iot_devices (farmer_id, device_name, provider, provider_device_id, provider_config) 
                 VALUES ($1, $2, $3, $4, $5) RETURNING id`,
                ['11111111-1111-1111-1111-111111111111', 'Smart Pump 1', provider, providerDeviceId, credentials]
            );
            const internalId = res.rows[0].id;

            // Register with gateway memory
            await gateway.registerDevice(internalId, provider, credentials);
            await client.query('COMMIT');
            
            return { status: 'success', deviceId: internalId };
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    });

    // 3. Send Command (Starts Verification Pipeline)
    fastify.post('/devices/:id/command', async (request, reply) => {
        const { id } = request.params as { id: string };
        const { command } = request.body as { command: string };

        // 1. Insert into commands_queue with state 'pending'
        const client = await pool.connect();
        try {
            await client.query(
                `INSERT INTO iot_commands_queue (device_id, command, status) VALUES ($1, $2, 'pending')`,
                [id, command]
            );
            
            // 2. Instruct gateway to execute
            // We do not await verification here. We return 202 Accepted.
            gateway.executeCommand(id, command).catch(err => fastify.log.error(err));
            
            return reply.status(202).send({ status: 'pending_verification', message: 'Command dispatched. Awaiting telemetry verification.' });
        } finally {
            client.release();
        }
    });

    // 4. Get Connected Devices
    fastify.get('/devices', async (request, reply) => {
        const client = await pool.connect();
        try {
            const res = await client.query(`SELECT * FROM iot_devices`);
            return { status: 'success', devices: res.rows };
        } finally {
            client.release();
        }
    });
}
