'use strict';

module.exports = {
  testEnvironment: 'node',
  moduleFileExtensions: ['js', 'json', 'jsx', 'ts', 'tsx', 'node'],
  transform: {
    '^.+\.jsx?$': 'babel-jest',
  },
  extensionsToTreatAsEsm: ['.js'],
  globals: {
    'babel-jest': {
      presets: ['@babel/preset-env'],
    },
  },
};