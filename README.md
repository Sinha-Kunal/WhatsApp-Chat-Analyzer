# 📱 WhatsApp Chat Analyzer

A comprehensive Python tool to analyze WhatsApp chat exports with **54+ different analysis metrics**. Get deep insights into your conversations, messaging patterns, and user behavior.

## ✨ Features

### 📊 Basic Statistics
- Total messages, participants, and date range
- Average messages per day
- Author-wise message distribution

### ⏰ Time-Based Analysis
- **Activity by Hour** - Discover peak messaging hours
- **Activity by Day** - Find busiest days of the week
- **Monthly Trends** - Track conversation patterns over time
- **Peak Activity Finder** - Identify exact hour-day combinations with most activity
- **Weekend vs Weekday** - Compare messaging behavior
- **Night Owl Analysis** (12 AM - 5 AM)
- **Early Bird Analysis** (5 AM - 8 AM)
- **Seasonal Activity** - Activity patterns across seasons

### 👥 User Behavior
- **Author Statistics** - Messages, words, and contribution percentage per user
- **Message Length Analysis** - Average and longest messages by author
- **Response Time Analysis** - How quickly users respond
- **Reply Speed by Author** - Fastest responders
- **Author Response Rate** - How often each user replies to others
- **Conversation Starters** - Who initiates conversations most
- **Conversation Initiator by Time** - Who starts chats at different times
- **Author Consistency** - How regularly users participate
- **Engagement Score** - Composite metric of user engagement
- **Busiest Hour by Author** - Each person's most active time
- **Vocabulary Richness** - Unique word usage per author

### 💬 Message Content Analysis
- **Most Common Words** - Top frequently used words (with stop word filtering)
- **Word Cloud Data** - Export-ready data for visualization
- **Emoji Analysis** - Most used emojis with counts
- **Sentiment Keywords** - Positive vs negative word usage
- **Question Analysis** - Who asks the most questions
- **Media & Links** - Count of shared media and URLs
- **URL Domain Analysis** - Most shared websites
- **Message Type Breakdown** - Categorize by media, links, questions, etc.
- **Longest Messages** - Find the wordiest messages
- **Deleted Messages Analysis** - Track deleted content
- **Forwarded Message Analysis** - Identify forwarded content

### 🗣️ Communication Patterns
- **Author Interaction Matrix** - Who replies to whom most often
- **Who Talks to Whom** - Direct reply patterns
- **Conversation Burst Analysis** - Length of rapid-fire exchanges
- **Reply Chain Depth** - How long conversations go without breaks
- **Monologue Detection** - Longest consecutive messages by one person
- **Silence Periods** - Longest gaps in conversation
- **Streak Analysis** - Longest consecutive active days

### 🎭 Personality Insights
- **Laugh Analysis** - Different types of laughter (haha, lol, 😂, etc.)
- **Politeness Analysis** - Usage of please, thanks, sorry, etc.
- **CAPS LOCK Analysis** - Who "shouts" the most
- **Punctuation Personality** - Exclamation marks, ellipsis, etc.
- **@Mention Analysis** - Most mentioned users
- **Hashtag Analysis** - Popular hashtags

### 📈 Activity Metrics
- **Most Active Days** - Top 10 busiest dates
- **Unique Participant Daily** - Active users per day
- **Ghost Analysis** - Least active members
- **Time to First Message** - When the first message of the day arrives

## 🚀 Installation

### Prerequisites
```bash
python 3.7+
```

### Install Dependencies
```bash
pip install pandas matplotlib seaborn
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## 📝 Usage

### 1. Export Your WhatsApp Chat

**On Android:**
1. Open the chat
2. Tap ⋮ (three dots) → More → Export chat
3. Choose "Without Media"
4. Save the `.txt` file

**On iOS:**
1. Open the chat
2. Tap contact/group name → Export Chat
3. Choose "Without Media"
4. Save the `.txt` file

### 2. Run the Analyzer

```python
from whatsapp_analyzer import WhatsAppAnalyzer

# Initialize with your chat file
analyzer = WhatsAppAnalyzer('WhatsApp Chat.txt')

# Run all analyses
analyzer.run_all_analyses()

# Or run specific analyses
analyzer.basic_stats()
analyzer.emoji_analysis()
analyzer.activity_by_time()
```

## 📋 Example Output

```
============================================================
WHATSAPP CHAT ANALYSIS
============================================================

Total Messages: 15,432
Total Participants: 8
Date Range: 2023-01-15 to 2024-11-30
Total Days: 685
Average Messages per Day: 22.53

============================================================
AUTHOR STATISTICS
============================================================
                    Messages  Total Words  Avg Words/Message  % of Total
Alice                  5234        42187              8.06       33.92
Bob                    4123        31456              7.63       26.72
Charlie                2891        18934              6.55       18.74
...

============================================================
EMOJI ANALYSIS
============================================================
Total Emojis: 2,847

Top 15 Emojis:
😂 : 456
❤️ : 234
👍 : 189
...
```

## 🎯 Analysis Methods

| Method | Description |
|--------|-------------|
| `basic_stats()` | Overview statistics |
| `author_stats()` | Per-user message analysis |
| `activity_by_time()` | Hourly activity patterns |
| `emoji_analysis()` | Emoji usage breakdown |
| `sentiment_keywords()` | Positive/negative sentiment |
| `response_time_analysis()` | Average reply times |
| `conversation_starters()` | Who initiates conversations |
| `night_owl_analysis()` | Late night activity (12AM-5AM) |
| `laugh_analysis()` | Types of laughter expressions |
| `author_interaction_matrix()` | Reply patterns between users |
| `run_all_analyses()` | Execute all 54 analyses |

## 📊 Supported Chat Formats

The analyzer supports WhatsApp chat exports in the format:
```
DD/MM/YYYY, HH:MM - Username: Message
```

Example:
```
25/12/2024, 14:30 - Alice: Hello everyone!
25/12/2024, 14:31 - Bob: Hi Alice! How are you?
```

## 🛠️ Customization

You can customize various parameters:

```python
# Show top 15 instead of default 10
analyzer.most_active_days(top_n=15)

# Analyze top 30 words
analyzer.most_common_words(top_n=30)

# Find top 5 longest messages
analyzer.find_longest_messages(top_n=5)
```

## 📈 Advanced Features

### Word Cloud Generation
Export word frequency data for creating word clouds:
```python
analyzer.word_cloud_data(top_n=100)
```

### Custom Stop Words
Modify the stop words list in `most_common_words()` method to filter domain-specific terms.

### Time Gap Customization
Adjust conversation break thresholds in methods like `conversation_starters()` and `conversation_length_analysis()`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Privacy Notice

This tool processes chat data **locally on your machine**. No data is sent to external servers. Always respect privacy when analyzing group chats and obtain consent from participants if sharing insights.

## 🐛 Known Issues

- Very large chat files (>100MB) may require significant processing time
- Some special characters in usernames may cause parsing issues
- Non-English messages are supported but word frequency analysis works best with English

## 🔮 Roadmap

- [ ] Export results to HTML/PDF reports
- [ ] Interactive visualization dashboard
- [ ] Support for Telegram exports
- [ ] Sentiment analysis using ML models
- [ ] Network graph visualization of interactions
- [ ] Comparative analysis between multiple chats

## 💡 Tips

- **Large Files**: For very large chats, run individual analyses instead of `run_all_analyses()`
- **Performance**: The tool is optimized for chats up to 50,000 messages
- **Accuracy**: Ensure your chat export follows WhatsApp's standard format

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

## 🌟 Acknowledgments

- Built with Python, Pandas, and love for data analysis
- Inspired by the need to understand our digital conversations better

---

**Made with ❤️ for chat enthusiasts and data nerds**

*Star ⭐ this repo if you find it useful!*
