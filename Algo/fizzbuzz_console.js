/**
 * ==============================
 * FizzBuzz - Fulll hiring test
 * ==============================
 * > Thomas Rigole
 * ------------------------------
 */

/**
 * Generates sequences of values/words based on the fizzbuzzMap ruleset.
 * 
 * @param {number} n - Upper bound of the FizzBuzz algorithm
 * @param {Object} fizzbuzzMap - Ruleset composed of divisor(s) and associated word(s)
 */
function fizzbuzzGenerator(n, fizzbuzzMap) {
    for (let i = 1; i <= n; i++) {
        let sequence = '';
        for (const [divisor, word] of Object.entries(fizzbuzzMap)) {
            if (i % divisor === 0) {
                sequence += word;
            }
        }

        // Console prompt
        console.log(sequence || i);
    }
}

/**
 * Main function - FizzBuzz program
 */
function main() {
    // Input N
    let n = Number(prompt("Enter the upper bound N: "));

    // Input validation
    if (!Number.isInteger(n) || n <= 0) {
        console.error("Invalid input. Please enter a positive integer.");
        return;  // Exit if error (invalid format)
    }

    // FizzBuzz ruleset
    const fizzbuzzMap = {3: 'Fizz', 5: 'Buzz'};

    // Sequence generation
    fizzbuzzGenerator(n, fizzbuzzMap);
}

// Call the main function
main();
