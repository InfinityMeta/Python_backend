# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: iris.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\niris.proto\x12\x04iris\"j\n\x12IrisPredictRequest\x12\x14\n\x0csepal_length\x18\x01 \x01(\x01\x12\x13\n\x0bsepal_width\x18\x02 \x01(\x01\x12\x14\n\x0cpetal_length\x18\x03 \x01(\x01\x12\x13\n\x0bpetal_width\x18\x04 \x01(\x01\"#\n\x10IrisPredictReply\x12\x0f\n\x07species\x18\x01 \x01(\t2Y\n\rIrisPredictor\x12H\n\x12PredictIrisSpecies\x12\x18.iris.IrisPredictRequest\x1a\x16.iris.IrisPredictReply\"\x00\x42(\n\x13io.grpc.examples.mlB\tIrisProtoP\x01\xa2\x02\x03HLWb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'iris_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023io.grpc.examples.mlB\tIrisProtoP\001\242\002\003HLW'
  _globals['_IRISPREDICTREQUEST']._serialized_start=20
  _globals['_IRISPREDICTREQUEST']._serialized_end=126
  _globals['_IRISPREDICTREPLY']._serialized_start=128
  _globals['_IRISPREDICTREPLY']._serialized_end=163
  _globals['_IRISPREDICTOR']._serialized_start=165
  _globals['_IRISPREDICTOR']._serialized_end=254
# @@protoc_insertion_point(module_scope)
