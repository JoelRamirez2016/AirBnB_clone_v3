#!/usr/bin/python3
from models.state import State
from flask import Flask
from flask_restful import Resource, Api

class StateView(Resource):
    
