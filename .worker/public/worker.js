// Maximum value as a BigInt
const MAX_VALUE = BigInt("9999999999999999999999999999")

// Function to generate odd numbers less than MAX_VALUE
function* generateOddNumbers(max) {
  let current = BigInt(1) // Start from 1, the first odd number
  while (current < max) {
    yield current
    current += BigInt(2)
  }
}

// Function to check if a number is prime
function isPrime(num) {
  if (num % BigInt(2) === 0) return false
  for (let i = BigInt(3); i * i <= num; i += BigInt(2)) {
    if (num % i === 0) return false
  }
  return true
}

// Function to find the first prime number from the end
function findFirstPrimeFromEnd(max) {
  let current = max % BigInt(2) === 0 ? max - BigInt(1) : max // Ensure starting with an odd number
  while (current > 0) {
    if (isPrime(current)) {
      return current
    }
    current -= BigInt(2)
  }
  return null // No prime number found (unlikely for this range)
}

// Example usage: Iterating over even numbers less than MAX_VALUE
const evenNumbers = generateOddNumbers(MAX_VALUE)

self.onmessage = function (e) {
  const num = e.data
  const firstPrimeFromEnd = findFirstPrimeFromEnd(num)
  console.log(
    `First prime number from the end: ${firstPrimeFromEnd.toString()}`
  )
  self.postMessage({ firstPrimeFromEnd })
}

self.onerror = function (e) {
  console.log({ e })
}
