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
import typing
from baml_py.baml_py import FieldType, EnumValueBuilder, EnumBuilder, ClassBuilder
from baml_py.type_builder import TypeBuilder as _TypeBuilder, ClassPropertyBuilder
from .globals import DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME


class TypeBuilder(_TypeBuilder):
    def __init__(self):
        super().__init__(classes=set(
          ["Answer","ConditionAndDrug","Drug","Medication","PatientInfo","Query",]
        ), enums=set(
          []
        ), runtime=DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME)









__all__ = ["TypeBuilder"]