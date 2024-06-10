import { FastifyInstance } from 'fastify';
import { Static, Type } from '@sinclair/typebox';
import { StateService } from '../service/stateService';

export default async function stateController(fastify: FastifyInstance) {
  const stateService = new StateService();

  const CommandBody = Type.Object({
    command: Type.Union([
      Type.Literal('CALIB_DATA_TARGET'),
      Type.Literal('CALIB_DATA_DESTINATION'),
      Type.Literal('START_MACHINE'),
      Type.Literal('STOP_MACHINE'),
    ]),
  });

  type CommandBodyType = Static<typeof CommandBody>;

  const CommandReply = Type.Object({
    success: Type.Boolean(),
    message: Type.String(),
  });

  type CommandReplyType = Static<typeof CommandReply>;

  fastify.post<{ Body: CommandBodyType; Reply: CommandReplyType }>(
    '/command',
    {
      schema: {
        body: CommandBody,
        response: {
          200: CommandReply,
        },
      },
    },
    async (request, reply) => {
      const { command } = request.body;
      stateService.processStateCommand(command);
      reply.send({ success: true, message: `Command ${command} has been sent.` });
    },
  );

  const CalibrationData = Type.Object({
    upper: Type.String(),
    lower: Type.String(),
  });

  const GetStateReply = Type.Object({
    calibrated: Type.Boolean(),
    machine_state: Type.String(),
    calibration_data: Type.Object({
      target: CalibrationData,
      destination: CalibrationData,
    }),
  });

  type GetStateReplyType = Static<typeof GetStateReply>;

  fastify.get<{ Reply: GetStateReplyType }>(
    '/',
    {
      schema: {
        response: {
          200: GetStateReply,
        },
      },
    },
    async (_request, reply) => {
      reply.send(stateService.getState());
    },
  );
}
