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
    // Get the sequence container
    const sequenceContainer = document.getElementById("sequence");
    sequenceContainer.innerHTML = ''; // Clear previous sequences

    for (let i = 1; i <= n; i++) {
        let sequence = '';
        for (const [divisor, word] of Object.entries(fizzbuzzMap)) {
            if (i % divisor === 0) {
                sequence += word;
            }
        }
        
        // Append the sequence to the sequenceContainer
        const output = document.createElement('div');
        output.textContent = sequence || i;
        sequenceContainer.appendChild(output);
    }
}

/**
 * Main function - FizzBuzz program
 */
function main() {
    document.getElementById('submit').addEventListener('click', () => {
        // Input N
        const n = Number(document.getElementById('upper_bound').value);

        // Input validation
        if (!Number.isInteger(n) || n <= 0) {
            alert("Invalid input. Please enter a positive integer.");
        }

        // FizzBuzz ruleset
        const fizzbuzzMap = {3: 'Fizz', 5: 'Buzz'};

        // Sequence generation
        fizzbuzzGenerator(n, fizzbuzzMap);
    });
}

// Call the main function
main();
