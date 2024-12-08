from flask import Flask, render_template, request
app = Flask(__name__)

# Function to calculate hex, binary, and decimal values
def calculate_hex(bits, operation='set', register_size=32):
    try:
        register_size = int(register_size)
    except ValueError:
        raise ValueError("Register size must be a valid integer.")
    
    if register_size <= 0:
        raise ValueError("Register size must be greater than 0.")
        
    if any(bit < 0 or bit >= register_size for bit in bits):
        raise ValueError(f"Bits must be within 0-{register_size - 1} for the selected register size.")

    value = 0  # Initial value (for setting or testing bits)
    
    if operation == 'Set (OR - |)':
        for bit in bits:
            value |= (1 << bit)  # Set bits using OR
    elif operation == 'Clear (AND - &)':
        value = (1 << register_size) - 1  # All bits set initially
        for bit in bits:
            value &= ~(1 << bit)  # Clear bits using AND
    elif operation == 'Test (AND - &)':
        for bit in bits:
            value |= (1 << bit)  # Set bits for testing using AND
    elif operation == 'Clear (AND - &, Neg ~)':
        # Negation of the mask and then AND to clear
        value = (1 << register_size) - 1  # Set all bits initially
        for bit in bits:
            value &= ~(1 << bit)  # First clear the bit
        # Negate the value for the final result
        value = ~value & ((1 << register_size) - 1)  # Negation (inversion) and mask to register size

    # Convert to hex, binary, and decimal
    hex_value = hex(value)
    binary_value = bin(value)
    decimal_value = str(value)

    return hex_value, binary_value, decimal_value


# Home route
@app.route('/')
def index():
    return render_template('index.html')


# Calculation route
@app.route('/calculate', methods=['POST'])
def calculate():
    bits = [int(bit.strip()) for bit in request.form['bits'].split(',')]
    operation = request.form['operation']
    register_size = request.form['register_size']
    
    hex_value, binary_value, decimal_value = calculate_hex(bits, operation, register_size)
    
    return render_template('result.html', hex=hex_value, binary=binary_value, decimal=decimal_value)


if __name__ == '__main__':
    app.run(debug=True)
