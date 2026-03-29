'use strict';

const assert = require('assert');
const http = require('http');

const options = {
  hostname: 'localhost',
  port: 3000, // change to your server port
};

describe('Server Endpoints Tests', function () {
  it('should return 200 for GET /', function (done) {
    http.get(`${options.hostname}:${options.port}/`, (res) => {
      assert.strictEqual(res.statusCode, 200);
      done();
    });
  });

  it('should return 404 for unknown endpoints', function (done) {
    http.get(`${options.hostname}:${options.port}/unknown`, (res) => {
      assert.strictEqual(res.statusCode, 404);
      done();
    });
  });

  // Add more tests here for other endpoints
y
});
