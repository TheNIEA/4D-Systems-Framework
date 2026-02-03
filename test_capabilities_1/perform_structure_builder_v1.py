class ArithmeticPathwayBuilder:
    """
    A class that builds strong pathways for performing basic arithmetic operations.
    Provides methods for addition, subtraction, multiplication, division, and power operations
    with comprehensive error handling and validation.
    """
    
    def __init__(self):
        """Initialize the arithmetic pathway builder."""
        self.operation_history = []
    
    def add(self, a, b):
        """
        Perform addition of two numbers.
        
        Args:
            a (int, float): First operand
            b (int, float): Second operand
            
        Returns:
            int or float: Sum of a and b
            
        Raises:
            TypeError: If operands are not numeric types
        """
        try:
            self._validate_numeric_inputs(a, b)
            result = a + b
            self._log_operation('add', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Addition failed: {str(e)}")
    
    def subtract(self, a, b):
        """
        Perform subtraction of two numbers.
        
        Args:
            a (int, float): Minuend
            b (int, float): Subtrahend
            
        Returns:
            int or float: Difference of a and b
            
        Raises:
            TypeError: If operands are not numeric types
        """
        try:
            self._validate_numeric_inputs(a, b)
            result = a - b
            self._log_operation('subtract', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Subtraction failed: {str(e)}")
    
    def multiply(self, a, b):
        """
        Perform multiplication of two numbers.
        
        Args:
            a (int, float): First factor
            b (int, float): Second factor
            
        Returns:
            int or float: Product of a and b
            
        Raises:
            TypeError: If operands are not numeric types
        """
        try:
            self._validate_numeric_inputs(a, b)
            result = a * b
            self._log_operation('multiply', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Multiplication failed: {str(e)}")
    
    def divide(self, a, b):
        """
        Perform division of two numbers.
        
        Args:
            a (int, float): Dividend
            b (int, float): Divisor
            
        Returns:
            float: Quotient of a and b
            
        Raises:
            TypeError: If operands are not numeric types
            ZeroDivisionError: If divisor is zero
        """
        try:
            self._validate_numeric_inputs(a, b)
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            result = a / b
            self._log_operation('divide', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Division failed: {str(e)}")
        except ZeroDivisionError as e:
            raise ZeroDivisionError(f"Division failed: {str(e)}")
    
    def power(self, base, exponent):
        """
        Perform exponentiation operation.
        
        Args:
            base (int, float): Base number
            exponent (int, float): Exponent
            
        Returns:
            int or float: Result of base raised to the power of exponent
            
        Raises:
            TypeError: If operands are not numeric types
            OverflowError: If result is too large
        """
        try:
            self._validate_numeric_inputs(base, exponent)
            result = base ** exponent
            if not isinstance(result, (int, float)) or abs(result) == float('inf'):
                raise OverflowError("Result is too large to compute")
            self._log_operation('power', base, exponent, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Power operation failed: {str(e)}")
        except OverflowError as e:
            raise OverflowError(f"Power operation failed: {str(e)}")
    
    def modulo(self, a, b):
        """
        Perform modulo operation.
        
        Args:
            a (int, float): Dividend
            b (int, float): Divisor
            
        Returns:
            int or float: Remainder of a divided by b
            
        Raises:
            TypeError: If operands are not numeric types
            ZeroDivisionError: If divisor is zero
        """
        try:
            self._validate_numeric_inputs(a, b)
            if b == 0:
                raise ZeroDivisionError("Modulo by zero is not allowed")
            result = a % b
            self._log_operation('modulo', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Modulo operation failed: {str(e)}")
        except ZeroDivisionError as e:
            raise ZeroDivisionError(f"Modulo operation failed: {str(e)}")
    
    def chain_operations(self, initial_value, operations):
        """
        Perform a chain of arithmetic operations.
        
        Args:
            initial_value (int, float): Starting value
            operations (list): List of tuples (operation, operand) where operation is a string
            
        Returns:
            int or float: Final result after all operations
            
        Raises:
            TypeError: If initial value is not numeric or operations list is invalid
            ValueError: If operation is not supported
        """
        try:
            self._validate_numeric_inputs(initial_value, 0)  # Validate initial value
            if not isinstance(operations, list):
                raise TypeError("Operations must be provided as a list")
            
            result = initial_value
            operation_map = {
                'add': self.add,
                'subtract': self.subtract,
                'multiply': self.multiply,
                'divide': self.divide,
                'power': self.power,
                'modulo': self.modulo
            }
            
            for operation, operand in operations:
                if operation not in operation_map:
                    raise ValueError(f"Unsupported operation: {operation}")
                result = operation_map[operation](result, operand)
            
            return result
        except (TypeError, ValueError, ZeroDivisionError, OverflowError) as e:
            raise type(e)(f"Chain operation failed: {str(e)}")
    
    def get_operation_history(self):
        """
        Get the history of performed operations.
        
        Returns:
            list: List of operation records
        """
        return self.operation_history.copy()
    
    def clear_history(self):
        """Clear the operation history."""
        self.operation_history.clear()
    
    def _validate_numeric_inputs(self, a, b):
        """
        Validate that inputs are numeric types.
        
        Args:
            a: First input to validate
            b: Second input to validate
            
        Raises:
            TypeError: If inputs are not numeric types
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Operands must be numeric types (int or float)")
        
        if isinstance(a, bool) or isinstance(b, bool):
            raise TypeError("Boolean values are not allowed as operands")
    
    def _log_operation(self, operation, operand1, operand2, result):
        """
        Log the performed operation.
        
        Args:
            operation (str): Name of the operation
            operand1: First operand
            operand2: Second operand
            result: Result of the operation
        """
        self.operation_history.append({
            'operation': operation,
            'operand1': operand1,
            'operand2': operand2,
            'result': result
        })