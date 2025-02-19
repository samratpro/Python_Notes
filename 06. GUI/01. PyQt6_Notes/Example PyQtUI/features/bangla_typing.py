from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QLineEdit


def enable_bangla_typing(line_edit: QLineEdit, language="Bangla"):
    """
    Enables Bangla typing for the given QLineEdit widget by overriding its keyPressEvent.
    If the language is not "Bangla", the original keyPressEvent is restored.
    """
    if not line_edit:
        raise ValueError("QLineEdit widget is not valid!")

    # Store the original keyPressEvent method if not already stored
    if not hasattr(line_edit, "_original_keyPressEvent"):
        line_edit._original_keyPressEvent = line_edit.keyPressEvent

    def keyPressEvent(event: QKeyEvent):
        if language == "Bangla":
            shift_pressed = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
            ctrl_pressed = event.modifiers() & Qt.KeyboardModifier.ControlModifier
            # Bangla key mappings
            key_mappings = {
                Qt.Key.Key_Q: "ং" if shift_pressed else "ঙ",
                Qt.Key.Key_W: "য়" if shift_pressed else "য",
                Qt.Key.Key_E: "ঢ" if shift_pressed else "ড",
                Qt.Key.Key_R: "ফ" if shift_pressed else "প",
                Qt.Key.Key_T: "ঠ" if shift_pressed else "ট",
                Qt.Key.Key_Y: "ছ" if shift_pressed else "চ",
                Qt.Key.Key_U: "ঝ" if shift_pressed else "জ",
                Qt.Key.Key_I: "ঞ" if shift_pressed else "হ",
                Qt.Key.Key_O: "ঘ" if shift_pressed else "গ",
                Qt.Key.Key_P: "ঢ়" if shift_pressed else "ড়",
                Qt.Key.Key_A: "র্" if shift_pressed else "ৃ",
                Qt.Key.Key_S: "ূ" if shift_pressed else "ু",
                Qt.Key.Key_D: "ী" if shift_pressed else "ি",
                Qt.Key.Key_F: "অ" if shift_pressed else "া",
                Qt.Key.Key_G: "।" if shift_pressed else "্",
                Qt.Key.Key_H: "ভ" if shift_pressed else "ব",
                Qt.Key.Key_J: "খ" if shift_pressed else "ক",
                Qt.Key.Key_K: "থ" if shift_pressed else "ত",
                Qt.Key.Key_L: "ধ" if shift_pressed else "দ",
                Qt.Key.Key_Z: "্য" if shift_pressed else "্র",
                Qt.Key.Key_X: "ৗ" if shift_pressed else "ও",
                Qt.Key.Key_C: "ৈ" if shift_pressed else "ে",
                Qt.Key.Key_V: "ল" if shift_pressed else "র",
                Qt.Key.Key_B: "ণ" if shift_pressed else "ন",
                Qt.Key.Key_N: "ষ" if shift_pressed else "স",
                Qt.Key.Key_M: "শ" if shift_pressed else "ম",
                Qt.Key.Key_QuoteDbl: "”" if shift_pressed else "’",
                Qt.Key.Key_Space: " ",  # Space key
            }

            if ctrl_pressed:
                line_edit._original_keyPressEvent(event)
            elif event.key() in key_mappings:
                char = key_mappings[event.key()]

                # Handle space key separately
                if event.key() == Qt.Key.Key_Space:
                    line_edit.insert(" ")
                else:
                    # Handle vowel signs (া, ি, ী, ু, ূ, ে, ৈ, ো, ৌ, etc.)
                    if char in ["া", "ি", "ী", "ু", "ূ", "ে", "ৈ", "ো", "ৌ", "ৃ", "্য", "্র"]:
                        cursor_position = line_edit.cursorPosition()
                        if cursor_position > 0:
                            # Get the character before the cursor
                            previous_char = line_edit.text()[cursor_position - 1]
                            combined_char = combine_vowel_sign(previous_char, char)
                            # Replace the previous character with the combined character
                            line_edit.setText(line_edit.text()[:cursor_position - 1] + combined_char + line_edit.text()[cursor_position:])
                            # Move the cursor to the right after inserting the vowel sign
                            line_edit.setCursorPosition(cursor_position + 2)
                        else:
                            # If there's no previous character, just insert the vowel sign
                            line_edit.insert(char)
                            # Move the cursor to the right after inserting the vowel sign
                            line_edit.setCursorPosition(line_edit.cursorPosition() + 1)
                    else:
                        # Insert the character at the cursor position
                        line_edit.insert(char)
            else:
                line_edit._original_keyPressEvent(event)
        else:
            # If the language is not Bangla, restore the original keyPressEvent
            line_edit.keyPressEvent = line_edit._original_keyPressEvent
            line_edit._original_keyPressEvent(event)

    # Replace the keyPressEvent of the QLineEdit widget
    if language == "Bangla":
        line_edit.keyPressEvent = keyPressEvent
    else:
        # Restore the original keyPressEvent if the language is not Bangla
        line_edit.keyPressEvent = line_edit._original_keyPressEvent


def combine_vowel_sign(consonant: str, vowel_sign: str) -> str:
    """
    Combine a consonant with a vowel sign.
    """
    combinations = {
        ("অ", "া"): "আ",
        ("্", "ি"): "ই",
        ("্", "ী"): "ঈ",
        ("্", "ু"): "উ",
        ("্", "ূ"): "ঊ",
        ("্", "ৃ"): "ঋ",
        ("্", "ে"): "এ",
        ("্", "ৈ"): "ঐ",
        ("ও", "ো"): "ও",
        ("ও", "ৗ"): "ঔ"
    }
    return combinations.get((consonant, vowel_sign), consonant + vowel_sign)