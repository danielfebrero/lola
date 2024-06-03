'use strict'

const abind = require('abind')

class Talker {
  constructor (name) {
    this.name = name
    abind(this)
  }

  sayHi () {
    return `Hi, i'm ${this.name}`
  }
}

let { sayHi } = new Talker('Tom')

console.log(sayHi()) // -> Hi, i'm Tom
