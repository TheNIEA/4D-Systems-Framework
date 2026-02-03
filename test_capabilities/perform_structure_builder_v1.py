class ArithmeticOperationsBuilder:
    """A class that builds strong pathways for performing basic arithmetic operations."""
    
    def __init__(self):
        """Initialize the arithmetic operations builder."""
        self.operation_history = []
    
    def add(self, a, b):
        """
        Perform addition operation.
        
        Args:
            a: First number (int or float)
            b: Second number (int or float)
            
        Returns:
            Sum of a and b
            
        Raises:
            TypeError: If inputs are not numeric
        """
        try:
            result = self._validate_numeric(a) + self._validate_numeric(b)
            self._log_operation('add', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for addition: {e}")
    
    def subtract(self, a, b):
        """
        Perform subtraction operation.
        
        Args:
            a: Minuend (int or float)
            b: Subtrahend (int or float)
            
        Returns:
            Difference of a and b
            
        Raises:
            TypeError: If inputs are not numeric
        """
        try:
            result = self._validate_numeric(a) - self._validate_numeric(b)
            self._log_operation('subtract', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for subtraction: {e}")
    
    def multiply(self, a, b):
        """
        Perform multiplication operation.
        
        Args:
            a: First factor (int or float)
            b: Second factor (int or float)
            
        Returns:
            Product of a and b
            
        Raises:
            TypeError: If inputs are not numeric
        """
        try:
            result = self._validate_numeric(a) * self._validate_numeric(b)
            self._log_operation('multiply', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for multiplication: {e}")
    
    def divide(self, a, b):
        """
        Perform division operation.
        
        Args:
            a: Dividend (int or float)
            b: Divisor (int or float)
            
        Returns:
            Quotient of a and b
            
        Raises:
            TypeError: If inputs are not numeric
            ZeroDivisionError: If divisor is zero
        """
        try:
            dividend = self._validate_numeric(a)
            divisor = self._validate_numeric(b)
            
            if divisor == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            
            result = dividend / divisor
            self._log_operation('divide', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for division: {e}")
    
    def power(self, base, exponent):
        """
        Perform exponentiation operation.
        
        Args:
            base: Base number (int or float)
            exponent: Exponent (int or float)
            
        Returns:
            Base raised to the power of exponent
            
        Raises:
            TypeError: If inputs are not numeric
            OverflowError: If result is too large
        """
        try:
            base_val = self._validate_numeric(base)
            exp_val = self._validate_numeric(exponent)
            
            result = base_val ** exp_val
            
            if abs(result) > 1e308:
                raise OverflowError("Result too large to represent")
            
            self._log_operation('power', base, exponent, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for exponentiation: {e}")
    
    def modulo(self, a, b):
        """
        Perform modulo operation.
        
        Args:
            a: Dividend (int or float)
            b: Divisor (int or float)
            
        Returns:
            Remainder of a divided by b
            
        Raises:
            TypeError: If inputs are not numeric
            ZeroDivisionError: If divisor is zero
        """
        try:
            dividend = self._validate_numeric(a)
            divisor = self._validate_numeric(b)
            
            if divisor == 0:
                raise ZeroDivisionError("Modulo by zero is not allowed")
            
            result = dividend % divisor
            self._log_operation('modulo', a, b, result)
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for modulo: {e}")
    
    def chain_operations(self, initial_value, operations):
        """
        Perform a chain of operations on an initial value.
        
        Args:
            initial_value: Starting value (int or float)
            operations: List of tuples (operation_name, operand)
            
        Returns:
            Final result after all operations
            
        Raises:
            ValueError: If operation name is invalid
            TypeError: If inputs are not numeric
        """
        result = self._validate_numeric(initial_value)
        
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
                raise ValueError(f"Unknown operation: {operation}")
            
            result = operation_map[operation](result, operand)
        
        return result
    
    def get_operation_history(self):
        """
        Get the history of all operations performed.
        
        Returns:
            List of operation dictionaries
        """
        return self.operation_history.copy()
    
    def clear_history(self):
        """Clear the operation history."""
        self.operation_history.clear()
    
    def _validate_numeric(self, value):
        """
        Validate that a value is numeric.
        
        Args:
            value: Value to validate
            
        Returns:
            Numeric value
            
        Raises:
            TypeError: If value is not numeric
        """
        if not isinstance(value, (int, float)):
            try:
                return float(value)
            except (ValueError, TypeError):
                raise TypeError(f"Expected numeric value, got {type(value).__name__}")
        return value
    
    def _log_operation(self, operation, operand1, operand2, result):
        """
        Log an operation to the history.
        
        Args:
            operation: Operation name
            operand1: First operand
            operand2: Second operand
            result: Operation result
        """
        self.operation_history.append({
            'operation': operation,
            'operand1': operand1,
            'operand2': operand2,
            'result': result
        })