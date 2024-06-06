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
