#!/usr/bin/env python3
"""
String Reverser Script
Reverses strings using different methods
"""

import sys

def reverse_string_simple(text):
    """
    Reverse a string using Python's slice notation
    """
    return text[::-1]

def reverse_string_loop(text):
    """
    Reverse a string using a loop
    """
    reversed_text = ""
    for char in text:
        reversed_text = char + reversed_text
    return reversed_text

def reverse_string_builtin(text):
    """
    Reverse a string using built-in functions
    """
    return ''.join(reversed(text))

def reverse_words_in_string(text):
    """
    Reverse the order of words in a string
    """
    words = text.split()
    return ' '.join(reversed(words))

def reverse_each_word(text):
    """
    Reverse each word individually but keep word order
    """
    words = text.split()
    reversed_words = [word[::-1] for word in words]
    return ' '.join(reversed_words)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("String Reverser - Multiple Methods")
        print("=" * 40)
        print("Usage:")
        print("  python reverse_string.py <text>")
        print("  python reverse_string.py \"<text with spaces>\"")
        print()
        print("Examples:")
        print("  python reverse_string.py hello")
        print("  python reverse_string.py \"Hello World\"")
        print("  python reverse_string.py \"The quick brown fox\"")
        print()
        print("Interactive mode:")
        while True:
            try:
                user_input = input("Enter text to reverse (or 'quit' to exit): ")
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                if user_input.strip():
                    print_all_reversals(user_input)
                    print()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
        return
    
    # Get text from command line arguments
    text = ' '.join(sys.argv[1:])
    print_all_reversals(text)

def print_all_reversals(text):
    """Print all different types of string reversals"""
    print(f"Original text: '{text}'")
    print("-" * 50)
    
    # Method 1: Simple character reversal
    result1 = reverse_string_simple(text)
    print(f"1. Character reversal (slice):     '{result1}'")
    
    # Method 2: Loop reversal
    result2 = reverse_string_loop(text)
    print(f"2. Character reversal (loop):      '{result2}'")
    
    # Method 3: Built-in reversal
    result3 = reverse_string_builtin(text)
    print(f"3. Character reversal (builtin):   '{result3}'")
    
    # Method 4: Word order reversal
    result4 = reverse_words_in_string(text)
    print(f"4. Word order reversal:            '{result4}'")
    
    # Method 5: Each word reversed individually
    result5 = reverse_each_word(text)
    print(f"5. Each word reversed:             '{result5}'")
    
    # Verify all character reversals are the same
    if result1 == result2 == result3:
        print("\n✓ All character reversal methods produce the same result")
    else:
        print("\n⚠ Warning: Character reversal methods don't match!")

if __name__ == "__main__":
    main()