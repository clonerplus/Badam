import avro from 'avsc';

export default avro.Type.forSchema({
  type: 'record',
  name: 'message',
  fields: [
    {
      name: 'object_type',
      type: {type: 'enum', name: 'Type', symbols: ['MSG']}
    },
    {
      name: 'sender_id',
      type: 'string'
    },
    {
      name: 'body',
      type: 'string'
    }
  ]
});
