#!/usr/bin/python3
"""Module to create a flask route"""
from models.base_model import BaseModel
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
import models
