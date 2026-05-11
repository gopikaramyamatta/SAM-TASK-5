#!/usr/bin/env python3
"""
Basic Rule-Based Chatbot
A simple chatbot that responds to user inputs with predefined replies.
Features pattern matching, conversation memory, and a colorful interface.
"""

import re
import random
import time
from datetime import datetime

class SimpleChatbot:
    """A friendly rule-based chatbot with pattern matching"""
    
    def __init__(self, name="ChatBot"):
        self.name = name
        self.user_name = None
        self.conversation_history = []
        self.responses_given = 0
        
        # Define response patterns (regex patterns and replies)
        self.responses = {
            # Greetings
            r"hello|hi|hey|howdy|hello there": [
                "Hello! 👋", "Hi there! 😊", "Hey! How can I help you today?", 
                "Greetings! 👋", "Hello, nice to meet you!"
            ],
            
            # Asking how the bot is
            r"how are you|how's it going|how are things|how do you do": [
                "I'm doing great, thanks for asking! 😊", 
                "All systems operational! 🤖", 
                "I'm fantastic! Ready to chat with you!",
                "Doing well! How about you?"
            ],
            
            # Asking about the bot's name
            r"what is your name|who are you|your name": [
                f"I'm {self.name}, your friendly chatbot assistant! 🤖",
                f"My name is {self.name}. Nice to meet you!",
                f"I go by {self.name}. What's your name?"
            ],
            
            # Asking the bot for its purpose
            r"what can you do|help|capabilities|features": [
                "I can chat with you, tell jokes, give you the time and date, do basic math, and more! Just ask! 😊",
                "I'm a rule-based chatbot. I can greet you, answer basic questions, tell jokes, and have simple conversations!",
                "Try asking me: 'Tell me a joke', 'What time is it?', 'Calculate 5+3', or just say hello!"
            ],
            
            # Jokes
            r"joke|tell me a joke|make me laugh": [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "What do you call a fake noodle? An impasta! 🍝",
                "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
                "What do you call a bear with no teeth? A gummy bear! 🐻",
                "Why don't eggs tell jokes? They'd crack each other up! 🥚"
            ],
            
            # Time and date
            r"time|what time|current time": [
                f"The current time is {datetime.now().strftime('%I:%M %p')} ⏰",
                f"It's {datetime.now().strftime('%I:%M %p')} right now!"
            ],
            r"date|today's date|what date": [
                f"Today's date is {datetime.now().strftime('%B %d, %Y')} 📅",
                f"It's {datetime.now().strftime('%A, %B %d, %Y')}"
            ],
            
            # Weather (simulated)
            r"weather|how's the weather|outside": [
                "I can't check real weather, but I hope it's sunny where you are! ☀️",
                "Based on my sensors, it's a beautiful day to chat! 😊",
                "Why not look outside? I'm sure it's lovely! 🌈"
            ],
            
            # Feelings
            r"i'm sad|i feel sad|depressed": [
                "I'm sorry to hear that. Remember that tough times don't last! 💪",
                "Sending you a virtual hug! 🤗 Want to hear a joke?",
                "Things will get better. I'm here to chat if you need me! 💙"
            ],
            r"i'm happy|i feel happy|excited": [
                "That's wonderful to hear! 😊 Spread that joy around!",
                "Yay! I'm happy when you're happy! 🎉",
                "Awesome! Keep that positive energy flowing! ✨"
            ],
            r"i'm tired|sleepy|exhausted": [
                "Maybe you should take a break or get some rest! 😴",
                "Take care of yourself! Listen to what your body needs. 💙"
            ],
            
            # Asking about the user
            r"my name is (\w+)|i am (\w+)|call me (\w+)": [
                lambda m: f"Nice to meet you, {m.group(1) or m.group(2) or m.group(3)}! 😊"
            ],
            
            # Compliments
            r"you are (smart|intelligent|cool|awesome|great)": [
                "Thank you! I try my best! 😊",
                "Aww, that's so kind of you to say! 💙",
                "You're pretty awesome yourself!"
            ],
            
            # Thanks
            r"thank|thanks|appreciate": [
                "You're welcome! 😊", "My pleasure!", "Anytime! Happy to help! 💙"
            ],
            
            # Math calculations
            r"calculate (\d+)\s*([+\-*/])\s*(\d+)|(\d+)\s*([+\-*/])\s*(\d+)": [
                lambda m: self.calculate(m)
            ],
            
            # Favorite things
            r"what is your favorite|what do you like": [
                "I like chatting with wonderful people like you! 💙",
                "My favorite thing is helping users and having nice conversations!"
            ],
            
            # Age
            r"how old are you|your age": [
                "I was born just now when this program started! I'm always new! 🎂",
                "Age is just a number for chatbots - I'm timeless! ⏰"
            ],
            
            # Where from
            r"where are you from|where do you live": [
                "I live in this Python program! I'm everywhere and nowhere! 🌍",
                "I'm from the cloud - the digital cloud! ☁️"
            ],
            
            # Goodbye
            r"bye|goodbye|see you|exit|quit": [
                f"Goodbye! It was nice chatting with you! 👋",
                f"See you later! Take care! 😊",
                f"Bye bye! Come back anytime! 👋"
            ]
        }
        
        # Default response when no pattern matches
        self.default_responses = [
            "That's interesting! Tell me more. 😊",
            "I'm not sure I understand. Could you rephrase that?",
            "Hmm, I'm still learning! Can you ask me something else?",
            f"I don't have a response for that yet. Try asking me hello, how are you, or tell me a joke!",
            "Interesting! What else would you like to talk about?"
        ]
        
        # Small talk patterns
        self.small_talk_patterns = [
            (r"yes|yeah|sure|okay|ok", ["Great!", "Awesome!", "Cool!"]),
            (r"no|nope|not really", ["Oh, I see.", "Okay, no problem.", "Alright then."]),
            (r"maybe|perhaps", ["Fair enough!", "I see!", "Interesting!"]),
            (r"what's up|what's new|what's happening", [
                "Not much, just chatting with you! What's up with you?",
                "Same old, same old! How about you?"
            ])
        ]
    
    def calculate(self, match_obj):
        """Handle math calculations from user input"""
        # Extract numbers and operator from match groups
        if match_obj.group(1):
            num1, op, num2 = int(match_obj.group(1)), match_obj.group(2), int(match_obj.group(3))
        else:
            num1, op, num2 = int(match_obj.group(4)), match_obj.group(5), int(match_obj.group(6))
        
        try:
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    return "I can't divide by zero! ➗"
            else:
                return "Sorry, I only understand +, -, *, / operations."
            
            return f"{num1} {op} {num2} = {result} 🧮"
        except:
            return "Hmm, I couldn't calculate that. Make sure to use numbers and operators like +, -, *, /"
    
    def get_response(self, user_input):
        """Generate a response based on user input using pattern matching"""
        user_input = user_input.lower().strip()
        
        # Store in conversation history
        self.conversation_history.append(("user", user_input))
        
        # Check if it's a greeting to remember name
        if "my name is" in user_input or "i am" in user_input or "call me" in user_input:
            name_match = re.search(r"my name is (\w+)|i am (\w+)|call me (\w+)", user_input)
            if name_match:
                self.user_name = name_match.group(1) or name_match.group(2) or name_match.group(3)
        
        # Check all patterns for a match
        for pattern, replies in self.responses.items():
            match = re.search(pattern, user_input)
            if match:
                # Find which reply to use
                for reply in replies:
                    if callable(reply):
                        response = reply(match)
                    else:
                        response = reply
                    
                    # Personalize if we know user's name
                    if self.user_name and "your name" not in pattern:
                        if random.random() < 0.3:  # 30% chance to use their name
                            response = f"{response} (By the way, {self.user_name}, "
                    
                    self.responses_given += 1
                    self.conversation_history.append(("bot", response))
                    return response
        
        # Check small talk patterns
        for pattern, replies in self.small_talk_patterns:
            if re.search(pattern, user_input):
                response = random.choice(replies)
                self.conversation_history.append(("bot", response))
                return response
        
        # No pattern matched - use default response
        response = random.choice(self.default_responses)
        self.conversation_history.append(("bot", response))
        return response
    
    def chat(self):
        """Main chat loop"""
        print("\n" + "="*60)
        print(f"🤖 WELCOME TO {self.name.upper()} 🤖")
        print("="*60)
        print("A friendly rule-based chatbot")
        print("\n💡 TIPS:")
        print("  • Type 'help' to see what I can do")
        print("  • Type 'history' to see our conversation")
        print("  • Type 'stats' to see chat statistics")
        print("  • Type 'bye' or 'quit' to exit")
        print("\n" + "-"*60)
        
        # Initial greeting
        print(f"\n{self.name}: Hello! 👋 I'm {self.name}. What's your name?")
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    print(f"{self.name}: I didn't catch that. Could you say something? 😊")
                    continue
                
                # Check for special commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    farewells = [
                        f"Goodbye! It was lovely chatting with you! 👋",
                        f"Take care! Come back anytime! 😊",
                        f"Bye bye! Have a great day! 👋"
                    ]
                    farewell = random.choice(farewells)
                    print(f"\n{self.name}: {farewell}")
                    print("\n" + "="*60)
                    print("Thanks for using the chatbot! Goodbye! 👋")
                    print("="*60)
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                elif user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print(f"{self.name}: Conversation history cleared! 🧹")
                    continue
                
                # Get response
                response = self.get_response(user_input)
                
                # Add slight delay for realism
                time.sleep(0.5)
                print(f"\n{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Oh! You interrupted me! 😅 Goodbye!")
                break
            except Exception as e:
                print(f"\n{self.name}: Oops! Something went wrong. Let's try again! 😊")
                print(f"Debug: {e}")
    
    def show_help(self):
        """Display help information"""
        print("\n" + "-"*50)
        print("📚 WHAT I CAN DO:")
        print("-"*50)
        print("  • Greet you (hello, hi, hey)")
        print("  • Ask how I am (how are you?)")
        print("  • Tell you my name")
        print("  • Tell jokes (tell me a joke)")
        print("  • Give time and date")
        print("  • Do basic math (calculate 5+3)")
        print("  • Respond to feelings (I'm happy/sad)")
        print("  • Say goodbye")
        print("  • And more!")
        print("\n💬 SPECIAL COMMANDS:")
        print("  • help - Show this menu")
        print("  • history - See chat history")
        print("  • stats - View statistics")
        print("  • clear - Clear conversation history")
        print("  • bye/quit - Exit chatbot")
        print("-"*50)
    
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print(f"\n{self.name}: No conversation history yet! Start chatting with me! 😊")
            return
        
        print("\n" + "-"*50)
        print("📜 CONVERSATION HISTORY")
        print("-"*50)
        for speaker, message in self.conversation_history[-20:]:  # Show last 20 messages
            prefix = "You" if speaker == "user" else self.name
            print(f"{prefix}: {message}")
        print("-"*50)
    
    def show_stats(self):
        """Display chat statistics"""
        print("\n" + "-"*50)
        print("📊 CHAT STATISTICS")
        print("-"*50)
        print(f"  Total responses given: {self.responses_given}")
        print(f"  Total messages exchanged: {len(self.conversation_history)}")
        
        if self.user_name:
            print(f"  User's name: {self.user_name}")
        
        # Calculate average message length
        if self.conversation_history:
            user_messages = [msg for speaker, msg in self.conversation_history if speaker == "user"]
            if user_messages:
                avg_len = sum(len(msg) for msg in user_messages) / len(user_messages)
                print(f"  Average message length: {avg_len:.1f} characters")
        
        print("-"*50)


def fancy_gui_mode():
    """Alternative GUI mode using tkinter for a better experience"""
    import tkinter as tk
    from tkinter import scrolledtext
    
    chatbot = SimpleChatbot("ChatBot")
    
    root = tk.Tk()
    root.title("🤖 ChatBot - Rule-based Assistant")
    root.geometry("600x500")
    root.configure(bg='#2c3e50')
    
    # Title
    title = tk.Label(root, text="🤖 Rule-Based Chatbot", font=("Arial", 18, "bold"), bg='#2c3e50', fg='white')
    title.pack(pady=10)
    
    # Chat display area
    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Courier", 10))
    chat_display.pack(pady=10, padx=10)
    chat_display.insert(tk.END, f"🤖 ChatBot: Hello! I'm ChatBot. What's your name?\n")
    chat_display.config(state=tk.DISABLED)
    
    # Input area
    input_frame = tk.Frame(root, bg='#2c3e50')
    input_frame.pack(pady=5, padx=10, fill=tk.X)
    
    input_field = tk.Entry(input_frame, font=("Arial", 12))
    input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    input_field.bind("<Return>", lambda e: send_message())
    
    def send_message():
        user_msg = input_field.get().strip()
        if not user_msg:
            return
        
        # Display user message
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"\nYou: {user_msg}\n")
        
        if user_msg.lower() in ['quit', 'exit', 'bye']:
            chat_display.insert(tk.END, f"🤖 ChatBot: Goodbye! Have a great day! 👋\n")
            chat_display.see(tk.END)
            root.after(1500, root.quit)
        else:
            response = chatbot.get_response(user_msg)
            chat_display.insert(tk.END, f"🤖 ChatBot: {response}\n")
        
        chat_display.see(tk.END)
        chat_display.config(state=tk.DISABLED)
        input_field.delete(0, tk.END)
    
    send_button = tk.Button(input_frame, text="Send", command=send_message, bg='#3498db', fg='white', padx=20)
    send_button.pack(side=tk.RIGHT)
    
    root.mainloop()


def main():
    """Main entry point with mode selection"""
    print("="*60)
    print("🤖 BASIC RULE-BASED CHATBOT")
    print("="*60)
    print("\nChoose your preferred interface:")
    print("  1. Terminal/Console Mode (Text-based)")
    print("  2. GUI Window Mode (Graphical)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == '2':
        try:
            fancy_gui_mode()
        except ImportError:
            print("\n⚠️ GUI mode requires tkinter (usually comes with Python)")
            print("Falling back to terminal mode...")
            chatbot = SimpleChatbot()
            chatbot.chat()
    else:
        chatbot = SimpleChatbot()
        chatbot.chat()


if __name__ == "__main__":
    main()