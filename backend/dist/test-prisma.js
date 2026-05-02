"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const client_1 = require("@prisma/client");
const prisma = new client_1.PrismaClient();
async function main() {
    try {
        const users = await prisma.user.findMany();
        console.log('Users:', users);
    }
    catch (e) {
        console.error('Error during findMany:', e);
    }
    finally {
        await prisma.$disconnect();
    }
}
main();
