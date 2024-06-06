(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// main.js
if (window.Worker) {
  const worker = new Worker("worker.js", { type: "module" })

  const MAX_VALUE = BigInt(
    "9999999999999999999999999999999999999999999999999999999999999999"
  )
  console.log(`WORK STARTING WITH MAX_VALUE=${MAX_VALUE}`)

  worker.postMessage(MAX_VALUE)

  worker.onmessage = function (e) {
    console.log(`Is ${e.data.firstPrimeFromEnd} a prime number? yes`)
  }

  worker.onerror = function (error) {
    console.log(`Worker error: ${JSON.stringify(error)}`)
  }
} else {
  console.log("Your browser doesn’t support web workers.")
}

},{}]},{},[1]);
