from doctest import debug
from typing import List, Optional
import sys
import math

def calculate_weighted_length(text: str) -> float:
    """
    Calculate the weighted length of text where spaces, commas, and dots count as 0.5
    and other characters count as 1.
    
    Args:
        text: The string to measure
        
    Returns:
        The weighted length as a float
    """
    length = 0.0
    for char in text:
        if char in ['.',"'"]:
            length += 0.25
        elif char in [' ', ',',';','"','-','!']:
            length += 0.5
        else:
            length += 1.0
    return length

def split_string_with_brackets(input_string: str):
    bracketed_content = None
    word_position_before_bracket = None
    text_without_brackets = input_string
    
    # Find parentheses content
    start_paren = input_string.find('(')
    if start_paren != -1:
        end_paren = input_string.find(')', start_paren)
        if end_paren != -1:
            # Extract the bracketed content including parentheses
            bracketed_content = input_string[start_paren:end_paren + 1]
            # Find which word position the bracket starts at
            text_before_bracket = input_string[:start_paren].strip()
            if text_before_bracket:
                words_before = text_before_bracket.split()
                word_position_before_bracket = len(words_before)
            else:
                word_position_before_bracket = 0
            
            # Remove bracketed content from string
            text_without_brackets = input_string[:start_paren].strip() + ' ' + input_string[end_paren + 1:].strip()
            text_without_brackets = ' '.join(text_without_brackets.split())  # Normalize spaces
            
            print(f"Found bracketed content: '{bracketed_content}' at word position {word_position_before_bracket}")
            print(f"Text without brackets: '{text_without_brackets}'")
    return text_without_brackets, bracketed_content, word_position_before_bracket

    

def split_string_by_length_internal(input_string: str, max_length: int, debug: bool = True) -> List[str]:
    """
    Internal method that returns chunks as a list without translation
    Uses weighted length where spaces, commas, dots = 0.5 and other chars = 1.0
    """
    if not input_string or max_length <= 0:
        return []
    
    input_weighted_len = calculate_weighted_length(input_string)
    
    # If string is shorter than max_length, return original string
    if input_weighted_len <= max_length:
        return [input_string]
    
    result = []
    pos = 0
    
    # Split the string respecting word boundaries
    while pos < len(input_string):
        # Find the position that gives us approximately max_length weighted characters
        chunk_end = pos
        current_weighted_length = 0.0
        
        # Advance character by character until we reach max weighted length
        while chunk_end < len(input_string) and current_weighted_length < max_length:
            char = input_string[chunk_end]
            if char in ["'",'.']:
                char_weight = 0.25
            elif char in [' ', ',',';','"','-','!']:
                char_weight = 0.5
            else:
                char_weight = 1.0
            
            if current_weighted_length + char_weight <= max_length:
                current_weighted_length += char_weight
                chunk_end += 1
            else:
                if debug:
                    print(f"Debug: pos={pos}, chunk_end={chunk_end}, weighted_len={current_weighted_length:.2f}, chunk='{input_string[pos:chunk_end]}'")
                break
            #print(f"Debug: char='{char}', weight={current_weighted_length}")
        
        # If we would go past the end, take everything remaining
        if chunk_end >= len(input_string):
            chunk_end = len(input_string)
        else:
            # Find the last space within the chunk to avoid splitting words
            original_chunk_end = chunk_end
            while chunk_end > pos and input_string[chunk_end] != ' ':
                chunk_end -= 1
            
            # If no space found, split at original position anyway (for very long words)
            if chunk_end == pos:
                chunk_end = original_chunk_end
        
        # Skip leading space if this isn't the first chunk
        if len(result) > 0 and pos < len(input_string) and input_string[pos] == ' ':
            pos += 1
            if pos >= chunk_end:
                continue
        
        # Include trailing space if present and within bounds
        if chunk_end < len(input_string) and input_string[chunk_end] == ' ':
            chunk_end += 1
        
        # Extract the chunk
        chunk = input_string[pos:chunk_end]
        chunk = chunk[::-1]
        chunk = chunk.strip()
        
        chunk_weighted_len = calculate_weighted_length(chunk)
        
        if debug:
            print(f"Debug: pos={pos}, chunk_end={chunk_end}, weighted_len={chunk_weighted_len:.2f}, chunk='{chunk}'")
        
        result.append(chunk)
        pos = chunk_end
    
    return result


def split_string(input: str, max_length: int, debug: bool = True):
        #print(f"Using max_length: {max_length}")

        #Step 1 - remove brackets and save it and its word index
        input_without_brackets, brackets, bracket_word_index = split_string_with_brackets(input)
        #Step 2 - split input_without_brackets to lines using max size of line
        chunks = split_string_by_length_internal(input_without_brackets, max_length, debug)
        if (len(chunks) == 1):
            chunks[0] = chunks[0][::-1]


        word_idx=0
        complete = ""
        prev_chunk = ""
        prev_chunk_index = -1
        #chunks.reverse()
        for chunk_index, chunk in enumerate(chunks):
            #print(f"chunk='{chunk}' len={len(chunk)}")
            if chunk_index==0:
                prev_chunk = chunk
                prev_chunk_index = chunk_index
                continue
            padding_needed = 26.5 - calculate_weighted_length(prev_chunk)
            padding_to_add = 0
            if debug:
                print(f"Debug: padding_needed={padding_needed:.2f}")
            padding_chars = int(int(padding_needed)/2)
            if padding_chars > 0: 
                if padding_needed != int(padding_needed):
                    prev_chunk = prev_chunk + ' '
                    padding_to_add += 0.5
                if int(padding_needed)/2 != int(int(padding_needed)/2):
                    prev_chunk = ' ' + prev_chunk + ' '
                    padding_to_add += 1
            # Calculate padding chars for each side (before and after)
            
            prev_chunk = '~' * padding_chars + prev_chunk + '~' * padding_chars
            padding_to_add += padding_chars
            if (padding_to_add > padding_needed):
                prev_chunk = prev_chunk.replace(' ', '', 1)
            chunks[prev_chunk_index] = prev_chunk
            prev_chunk = chunk
            prev_chunk_index = chunk_index
        #print(f"|{complete}|")

        # Concatenate all chunks into one string
        #chunks.reverse()

        # Replace space sequences with special characters in all chunks
        for i, chunk in enumerate(chunks):
            # Replace 3 spaces with 'Š' first (to avoid conflicts with 2-space replacement)
            #chunk = chunk.replace('   ', '~~~')
            # Replace 2 spaces with '€'
            #chunk = chunk.replace('  ', '~~')
            chunks[i] = chunk
            if (debug):
                print(f"Chunk {i} after replacement: '{chunk}' len={len(chunk)} calc={calculate_weighted_length(chunk)}")
        
        final_result = ' '.join(chunks)
        return final_result
        #print(f"Final concatenated result: '{final_result}'")
        #print(f"Length: {len(final_result)}")


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) == 2:
        max_length = int(sys.argv[1])
        # No arguments - run test cases with default values
        result = split_string("אני לא יודע את הרוע המשעבד אותך, שרה, אבל אני נשבע להביס אותו ולשחרר את נשמתך המתוקה.", max_length, True)
        print(f"Test 1 Result: '{result}'")
        
        result = split_string("אלמנת ברק, אני מתחייב בחיי שגם את וגם שרה תצעדנה על אדמתנו היפה שוב.", max_length, True)
        print(f"Test 2 Result: '{result}'")
        
        
        result = split_string("אחרי שהוא נמוג, בזמן שהייתי מבולבל ומבולבל לרגע, מכשפת ביצה מרושעת זחלה מהבריכה ההיא וגנבה את הקרן שלי. אובדנה הפך אותי לחיה מכוערת מאוד, כפי שאתה יכול לראות בבירור.", max_length, False)
        print(f"Test 3 Result: '{result}'")
        
        result = split_string("אני קוסם, בחור", max_length, False)
        print(f"Test 4 Result: '{result}'")        
        
        result = split_string("00 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0", max_length, True)
        print(f"Test 4 Result: '{result}'")        

        result = split_string("00 11 22 33 44 55 66 77 88 99 00 11 22 33", max_length, True)
        print(f"Test 4 Result: '{result}'")        

        result = split_string("0000 1111 2222 3333 4444 5555 6666 7777", max_length, True)
        print(f"Test 4 Result: '{result}'")        

        result = split_string("00000 11111 22222 33333 44444 55555", max_length, True)
        print(f"Test 4 Result: '{result}'")        

        result = split_string("000000 111111 222222 333333 444444", max_length, True)
        print(f"Test 4 Result: '{result}'")        

        result = split_string("0000000 1111111 2222222 3333333 4444444", max_length, True)
        print(f"Test 4 Result: '{result}'")        
        
        result = split_string("ג'וליה מסכנה; את היית שם בשבילי כשהיו לי בעיות. עכשיו את צריכה אותי. אני אתמיד עד שאת תשתחררי מהרוע הנורא הזה.",max_length, True)
        print(f"Test 4 Result: '{result}'")

        result = split_string("מר קאוונאג, אני מזועזע מגורלך. אני מבטיח לעשות כל מה שאני יכול כדי להציל אותך מעינוי נוסף.",max_length, True)
        print(f"Test 4 Result: '{result}'")

        result = split_string("בריאן ומרתה לין - בריאן לין ואשתו ואם אשתו, כולם חצו את הגשר יחד. הגשר קרס וכולם נפלו פנימה -- \"נלך הביתה במים,\" אמר בריאן לין.",max_length, True)
        print(f"Test 4 Result: '{result}'")

        result = split_string("אפילו כומר לא חסין מהמחלה המרושעת הזו המדביקה אותנו! אני נשבע, אבי, שתצעד על אדמתנו היפה שוב כל עוד יש בי נשימה!", max_length, True)
        print(f"Test 4 Result: '{result}'")

        result = split_string("אוי לי!... מפלצת אפלה! לא הייתה זו בשר ודם! מה עכשיו?",max_length, True)
        print(f"Test 4 Result: '{result}'")

        result = split_string("תחיה לצעוד על האדמה הירוקה של דאוונטרי שוב. אני מבטיח לך את זה!",max_length, True)
        print(f"Test 4 Result: '{result}'")        

        result = split_string("יוסף, חברי... אתה ואני עבדנו זה לצד זה. אתה איש טוב, ואני אתמיד לשחרר אותך מהכלא המרושע הזה.",max_length, True)
        print(f"Test 4 Result: '{result}'")

        result = split_string("זה היה כישוף של אפלה. מסכת הנצח ספגה גורל נורא; היא נופצה על ידי ישות רעה אשר מאז קבעה את משכנה במקדש הקדוש של המסכה.",max_length, True)
        print(f"Test 4 Result: '{result}'")

        result = split_string("אהה! יש לי את זה! הדיפיברילטור האלקטרומגנטי הטרה-קוסמי שלי! בעזרתו, אוכל להזיז את הקוטב המגנטי של כדור הארץ במעט... ולננו-שנייה בלבד. אבל זה יספיק! זה יערים על המפה שלך ויספק נקודת מסע חדשה. הקושי היחיד הוא...", max_length, True)
        print(f"Test 4 Result: '{result}'")