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
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Dict, Generic, List, Optional, TypeVar, Union, Literal

from . import types
from .types import Checked, Check

###############################################################################
#
#  These types are used for streaming, for when an instance of a type
#  is still being built up and any of its fields is not yet fully available.
#
###############################################################################

T = TypeVar('T')
class StreamState(BaseModel, Generic[T]):
    value: T
    state: Literal["Pending", "Incomplete", "Complete"]


class Answer(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

class ConditionAndDrug(BaseModel):
    condition: Optional[str] = None
    drug: List["types.Drug"]
    side_effects: List[str]

class Drug(BaseModel):
    generic_name: Optional[str] = None
    brand_names: List[str]

class Medication(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None

class PatientInfo(BaseModel):
    patient_id: Optional[str] = None
    medication: Optional["Medication"] = None
    side_effects: List[str]

class Query(BaseModel):
    query: Optional[str] = None
