import fastify from 'fastify';
import cors from '@fastify/cors';
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
import router from './router';

const server = fastify({
  logger: !!(process.env.NODE_ENV !== 'development'),
}).withTypeProvider<TypeBoxTypeProvider>();

server.register(cors);
server.register(router);

export default server;
