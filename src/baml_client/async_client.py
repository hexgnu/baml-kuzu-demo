###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
from typing import Any, Dict, List, Optional, TypeVar, Union, TypedDict, Type, Literal, cast
from typing_extensions import NotRequired
import pprint

import baml_py
from pydantic import BaseModel, ValidationError, create_model

from . import partial_types, types
from .types import Checked, Check
from .type_builder import TypeBuilder
from .globals import DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_CTX, DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME


OutputType = TypeVar('OutputType')


# Define the TypedDict with optional parameters having default values
class BamlCallOptions(TypedDict, total=False):
    tb: NotRequired[TypeBuilder]
    client_registry: NotRequired[baml_py.baml_py.ClientRegistry]
    collector: NotRequired[Union[baml_py.baml_py.Collector, List[baml_py.baml_py.Collector]]]
class BamlAsyncClient:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager
    __stream_client: "BamlStreamClient"

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager
      self.__stream_client = BamlStreamClient(self.__runtime, self.__ctx_manager)

    @property
    def stream(self):
      return self.__stream_client


    
    async def ExtractFromImage(
        self,
        img: baml_py.Image,
        baml_options: BamlCallOptions = {},
    ) -> List[types.ConditionAndDrug]:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = await self.__runtime.call_function(
        "ExtractFromImage",
        {
          "img": img,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(List[types.ConditionAndDrug], raw.cast_to(types, types, partial_types, False))
    
    async def ExtractMedicationInfo(
        self,
        notes: str,
        baml_options: BamlCallOptions = {},
    ) -> List[types.PatientInfo]:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = await self.__runtime.call_function(
        "ExtractMedicationInfo",
        {
          "notes": notes,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(List[types.PatientInfo], raw.cast_to(types, types, partial_types, False))
    
    async def RAGAnswerQuestion(
        self,
        question: str,context: str,
        baml_options: BamlCallOptions = {},
    ) -> types.Answer:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = await self.__runtime.call_function(
        "RAGAnswerQuestion",
        {
          "question": question,"context": context,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.Answer, raw.cast_to(types, types, partial_types, False))
    
    async def RAGText2Cypher(
        self,
        schema: str,question: str,
        baml_options: BamlCallOptions = {},
    ) -> types.Cypher:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = await self.__runtime.call_function(
        "RAGText2Cypher",
        {
          "schema": schema,"question": question,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.Cypher, raw.cast_to(types, types, partial_types, False))
    


class BamlStreamClient:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager

    
    def ExtractFromImage(
        self,
        img: baml_py.Image,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlStream[List[partial_types.ConditionAndDrug], List[types.ConditionAndDrug]]:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = self.__runtime.stream_function(
        "ExtractFromImage",
        {
          "img": img,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlStream[List[partial_types.ConditionAndDrug], List[types.ConditionAndDrug]](
        raw,
        lambda x: cast(List[partial_types.ConditionAndDrug], x.cast_to(types, types, partial_types, True)),
        lambda x: cast(List[types.ConditionAndDrug], x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )
    
    def ExtractMedicationInfo(
        self,
        notes: str,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlStream[List[partial_types.PatientInfo], List[types.PatientInfo]]:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = self.__runtime.stream_function(
        "ExtractMedicationInfo",
        {
          "notes": notes,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlStream[List[partial_types.PatientInfo], List[types.PatientInfo]](
        raw,
        lambda x: cast(List[partial_types.PatientInfo], x.cast_to(types, types, partial_types, True)),
        lambda x: cast(List[types.PatientInfo], x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )
    
    def RAGAnswerQuestion(
        self,
        question: str,context: str,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlStream[partial_types.Answer, types.Answer]:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = self.__runtime.stream_function(
        "RAGAnswerQuestion",
        {
          "question": question,
          "context": context,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlStream[partial_types.Answer, types.Answer](
        raw,
        lambda x: cast(partial_types.Answer, x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.Answer, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )
    
    def RAGText2Cypher(
        self,
        schema: str,question: str,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlStream[partial_types.Cypher, types.Cypher]:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)
      collector = baml_options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []
      raw = self.__runtime.stream_function(
        "RAGText2Cypher",
        {
          "schema": schema,
          "question": question,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlStream[partial_types.Cypher, types.Cypher](
        raw,
        lambda x: cast(partial_types.Cypher, x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.Cypher, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )
    

b = BamlAsyncClient(DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME, DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_CTX)

__all__ = ["b"]