import { FastifyInstance } from 'fastify';
import fastifyStatic from '@fastify/static';
import { resolve } from 'path';

export default async function indexController(fastify: FastifyInstance) {
  fastify.register(fastifyStatic, {
    root: resolve(__dirname, '../../../ui/dist/'),
    prefix: '/',
  });
}
