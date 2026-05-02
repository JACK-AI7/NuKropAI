import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  try {
    const users = await prisma.user.findMany();
    console.log('Users:', users);
  } catch (e) {
    console.error('Error during findMany:', e);
  } finally {
    await prisma.$disconnect();
  }
}

main();
