import { FastifyInstance } from 'fastify';
import queueController from './controller/queueController';
import indexController from './controller/indexController';
import stateController from './controller/stateController';

export default async function router(fastify: FastifyInstance) {
  fastify.register(indexController, { prefix: '/' });
  fastify.register(queueController, { prefix: '/queue' });
  fastify.register(stateController, { prefix: '/state' });
}
