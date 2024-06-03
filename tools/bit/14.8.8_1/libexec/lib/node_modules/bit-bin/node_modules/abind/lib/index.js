/**
 * Auto bind instance methods of classes.
 * @module abind
 * @version 1.0.5
 */

'use strict'

const abind = require('./abind')

let lib = abind.bind(this)

Object.assign(lib, abind, {
  abind
})

module.exports = lib
