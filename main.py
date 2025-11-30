import re
import pandas as pd
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

class WhatsAppAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.parse_chat()
    
    def parse_chat(self):
        """Parse WhatsApp chat export file"""
        pattern = r'(\d{2}/\d{2}/\d{4}),\s(\d{2}:\d{2})\s-\s([^:]+):\s(.+)'
        
        data = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(pattern, line.strip())
                if match:
                    date, time, author, message = match.groups()
                    data.append({
                        'date': date,
                        'time': time,
                        'author': author.strip(),
                        'message': message.strip()
                    })
        
        self.df = pd.DataFrame(data)
        self.df['datetime'] = pd.to_datetime(
            self.df['date'] + ' ' + self.df['time'], 
            format='%d/%m/%Y %H:%M'
        )
        self.df['date_only'] = self.df['datetime'].dt.date
        self.df['hour'] = self.df['datetime'].dt.hour
        self.df['day_of_week'] = self.df['datetime'].dt.day_name()
        self.df['month'] = self.df['datetime'].dt.to_period('M')
        self.df['word_count'] = self.df['message'].apply(lambda x: len(x.split()))
        
    def basic_stats(self):
        """Display basic statistics"""
        print("=" * 60)
        print("WHATSAPP CHAT ANALYSIS")
        print("=" * 60)
        print(f"\nTotal Messages: {len(self.df)}")
        print(f"Total Participants: {self.df['author'].nunique()}")
        print(f"Date Range: {self.df['datetime'].min().date()} to {self.df['datetime'].max().date()}")
        print(f"Total Days: {(self.df['datetime'].max() - self.df['datetime'].min()).days}")
        print(f"Average Messages per Day: {len(self.df) / max((self.df['datetime'].max() - self.df['datetime'].min()).days, 1):.2f}")
        
    def author_stats(self):
        """Analyze per-author statistics"""
        print("\n" + "=" * 60)
        print("AUTHOR STATISTICS")
        print("=" * 60)
        
        author_stats = self.df.groupby('author').agg({
            'message': 'count',
            'word_count': 'sum'
        }).sort_values('message', ascending=False)
        
        author_stats.columns = ['Messages', 'Total Words']
        author_stats['Avg Words/Message'] = (author_stats['Total Words'] / author_stats['Messages']).round(2)
        author_stats['% of Total'] = (author_stats['Messages'] / len(self.df) * 100).round(2)
        
        print(author_stats.to_string())
        
    def activity_by_time(self):
        """Analyze activity patterns by time"""
        print("\n" + "=" * 60)
        print("ACTIVITY BY HOUR")
        print("=" * 60)
        
        hourly = self.df.groupby('hour').size().sort_index()
        for hour, count in hourly.items():
            bar = '█' * int(count / hourly.max() * 50)
            print(f"{hour:02d}:00 | {bar} {count}")
        
    def activity_by_day(self):
        """Analyze activity patterns by day of week"""
        print("\n" + "=" * 60)
        print("ACTIVITY BY DAY OF WEEK")
        print("=" * 60)
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = self.df.groupby('day_of_week').size().reindex(day_order)
        
        for day, count in daily.items():
            bar = '█' * int(count / daily.max() * 50)
            print(f"{day:9s} | {bar} {count}")
    
    def most_active_days(self, top_n=10):
        """Find most active days"""
        print(f"\n" + "=" * 60)
        print(f"TOP {top_n} MOST ACTIVE DAYS")
        print("=" * 60)
        
        daily_activity = self.df.groupby('date_only').size().sort_values(ascending=False).head(top_n)
        
        for date, count in daily_activity.items():
            print(f"{date} | {count} messages")
    
    def media_and_links(self):
        """Analyze media and links"""
        print("\n" + "=" * 60)
        print("MEDIA & LINKS")
        print("=" * 60)
        
        media_count = self.df[self.df['message'].str.contains('<Media omitted>|image omitted|video omitted|audio omitted', case=False, na=False)].shape[0]
        links_count = self.df[self.df['message'].str.contains('http', case=False, na=False)].shape[0]
        
        print(f"Media Messages: {media_count}")
        print(f"Messages with Links: {links_count}")
    
    def most_common_words(self, top_n=20):
        """Find most common words"""
        print(f"\n" + "=" * 60)
        print(f"TOP {top_n} MOST COMMON WORDS")
        print("=" * 60)
        
        # Exclude common stop words and media messages
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'is', 'was', 'are', 'be', 'been', 'have', 'has', 'had',
                      'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                      'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that', 'these', 'those'}
        
        all_words = []
        for msg in self.df['message']:
            if not any(x in msg.lower() for x in ['<media omitted>', 'image omitted', 'video omitted']):
                words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
                all_words.extend([w for w in words if w not in stop_words])
        
        word_freq = Counter(all_words).most_common(top_n)
        
        for word, count in word_freq:
            bar = '█' * int(count / word_freq[0][1] * 40)
            print(f"{word:15s} | {bar} {count}")
    
    def emoji_analysis(self):
        """Analyze emoji usage"""
        print("\n" + "=" * 60)
        print("EMOJI ANALYSIS")
        print("=" * 60)
        
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        
        all_emojis = []
        for msg in self.df['message']:
            emojis = emoji_pattern.findall(msg)
            all_emojis.extend(emojis)
        
        if all_emojis:
            emoji_freq = Counter(all_emojis).most_common(15)
            print(f"Total Emojis: {len(all_emojis)}")
            print(f"\nTop 15 Emojis:")
            for emoji, count in emoji_freq:
                print(f"{emoji} : {count}")
        else:
            print("No emojis found in the chat.")
    
    def response_time_analysis(self):
        """Analyze average response times between users"""
        print("\n" + "=" * 60)
        print("RESPONSE TIME ANALYSIS")
        print("=" * 60)
        
        response_times = []
        for i in range(1, len(self.df)):
            if self.df.iloc[i]['author'] != self.df.iloc[i-1]['author']:
                time_diff = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 60
                if time_diff < 60:  # Only consider responses within 1 hour
                    response_times.append(time_diff)
        
        if response_times:
            print(f"Average Response Time: {sum(response_times) / len(response_times):.2f} minutes")
            print(f"Median Response Time: {sorted(response_times)[len(response_times)//2]:.2f} minutes")
        else:
            print("Not enough data for response time analysis")
    
    def conversation_starters(self, top_n=10):
        """Find who starts conversations most often"""
        print(f"\n" + "=" * 60)
        print(f"TOP {top_n} CONVERSATION STARTERS")
        print("=" * 60)
        
        starters = []
        for i in range(1, len(self.df)):
            time_gap = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 3600
            if time_gap > 4:  # 4 hour gap = new conversation
                starters.append(self.df.iloc[i]['author'])
        
        starter_counts = Counter(starters).most_common(top_n)
        for author, count in starter_counts:
            bar = '█' * int(count / starter_counts[0][1] * 40)
            print(f"{author[:25]:25s} | {bar} {count}")
    
    def message_length_analysis(self):
        """Analyze message length patterns"""
        print("\n" + "=" * 60)
        print("MESSAGE LENGTH ANALYSIS")
        print("=" * 60)
        
        length_stats = self.df.groupby('author')['word_count'].agg(['mean', 'median', 'max'])
        length_stats = length_stats.sort_values('mean', ascending=False)
        length_stats.columns = ['Avg Words', 'Median Words', 'Longest Message']
        
        print(length_stats.to_string())
    
    def deleted_messages_analysis(self):
        """Analyze deleted messages"""
        print("\n" + "=" * 60)
        print("DELETED MESSAGES ANALYSIS")
        print("=" * 60)
        
        deleted = self.df[self.df['message'].str.contains('deleted|This message was deleted', case=False, na=False)]
        
        if len(deleted) > 0:
            print(f"Total Deleted Messages: {len(deleted)}")
            print(f"\nDeleted by Author:")
            deleted_by_author = deleted.groupby('author').size().sort_values(ascending=False)
            for author, count in deleted_by_author.items():
                print(f"{author[:30]:30s} : {count}")
        else:
            print("No deleted messages found.")
    
    def question_analysis(self):
        """Analyze questions asked"""
        print("\n" + "=" * 60)
        print("QUESTION ANALYSIS")
        print("=" * 60)
        
        questions = self.df[self.df['message'].str.contains(r'\?', na=False)]
        
        print(f"Total Questions Asked: {len(questions)}")
        print(f"Percentage of Messages: {len(questions) / len(self.df) * 100:.2f}%")
        print(f"\nTop Question Askers:")
        
        question_askers = questions.groupby('author').size().sort_values(ascending=False).head(10)
        for author, count in question_askers.items():
            bar = '█' * int(count / question_askers.max() * 40)
            print(f"{author[:25]:25s} | {bar} {count}")
    
    def night_owl_analysis(self):
        """Find who chats late at night"""
        print("\n" + "=" * 60)
        print("NIGHT OWL ANALYSIS (12 AM - 5 AM)")
        print("=" * 60)
        
        night_messages = self.df[(self.df['hour'] >= 0) & (self.df['hour'] < 5)]
        
        if len(night_messages) > 0:
            print(f"Total Night Messages: {len(night_messages)}")
            print(f"Percentage of Total: {len(night_messages) / len(self.df) * 100:.2f}%")
            print(f"\nNight Owls:")
            
            night_owls = night_messages.groupby('author').size().sort_values(ascending=False).head(10)
            for author, count in night_owls.items():
                bar = '█' * int(count / night_owls.max() * 40)
                print(f"{author[:25]:25s} | {bar} {count}")
        else:
            print("No night messages found.")
    
    def ghost_analysis(self):
        """Find users who rarely message but are in chat"""
        print("\n" + "=" * 60)
        print("GHOST USERS (Least Active)")
        print("=" * 60)
        
        message_counts = self.df.groupby('author').size().sort_values()
        
        print(f"\nBottom 10 Users:")
        for author, count in message_counts.head(10).items():
            print(f"{author[:30]:30s} : {count} messages")
    
    def monthly_trend(self):
        """Analyze monthly message trends"""
        print("\n" + "=" * 60)
        print("MONTHLY MESSAGE TREND")
        print("=" * 60)
        
        monthly = self.df.groupby('month').size().sort_index()
        
        for month, count in monthly.items():
            bar = '█' * int(count / monthly.max() * 50)
            print(f"{month} | {bar} {count}")
    
    def streak_analysis(self):
        """Find longest active streaks"""
        print("\n" + "=" * 60)
        print("ACTIVITY STREAK ANALYSIS")
        print("=" * 60)
        
        dates = sorted(self.df['date_only'].unique())
        
        current_streak = 1
        max_streak = 1
        streak_end = dates[0]
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_streak += 1
                if current_streak > max_streak:
                    max_streak = current_streak
                    streak_end = dates[i]
            else:
                current_streak = 1
        
        print(f"Longest Active Streak: {max_streak} days")
        print(f"Streak Ended: {streak_end}")
    
    def author_interaction_matrix(self):
        """Who replies to whom most often"""
        print("\n" + "=" * 60)
        print("REPLY PATTERNS (Who replies to whom)")
        print("=" * 60)
        
        interactions = []
        for i in range(1, len(self.df)):
            if self.df.iloc[i]['author'] != self.df.iloc[i-1]['author']:
                time_diff = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 60
                if time_diff < 10:  # Reply within 10 minutes
                    interactions.append((self.df.iloc[i-1]['author'], self.df.iloc[i]['author']))
        
        if interactions:
            interaction_counts = Counter(interactions).most_common(15)
            print("\nTop 15 Reply Patterns:")
            for (from_user, to_user), count in interaction_counts:
                print(f"{from_user[:20]:20s} → {to_user[:20]:20s} : {count} times")
        else:
            print("Not enough data for interaction analysis")
    
    def weekend_vs_weekday(self):
        """Compare weekend vs weekday activity"""
        print("\n" + "=" * 60)
        print("WEEKEND VS WEEKDAY ACTIVITY")
        print("=" * 60)
        
        self.df['is_weekend'] = self.df['day_of_week'].isin(['Saturday', 'Sunday'])
        
        weekend = self.df[self.df['is_weekend']].shape[0]
        weekday = self.df[~self.df['is_weekend']].shape[0]
        
        total = weekend + weekday
        
        print(f"Weekday Messages: {weekday} ({weekday/total*100:.2f}%)")
        print(f"Weekend Messages: {weekend} ({weekend/total*100:.2f}%)")
        
        weekend_bar = '█' * int(weekend / total * 50)
        weekday_bar = '█' * int(weekday / total * 50)
        
        print(f"\nWeekday | {weekday_bar}")
        print(f"Weekend | {weekend_bar}")
    
    def find_longest_messages(self, top_n=5):
        """Find longest messages"""
        print(f"\n" + "=" * 60)
        print(f"TOP {top_n} LONGEST MESSAGES")
        print("=" * 60)
        
        longest = self.df.nlargest(top_n, 'word_count')
        
        for idx, row in longest.iterrows():
            print(f"\nAuthor: {row['author']}")
            print(f"Date: {row['datetime']}")
            print(f"Words: {row['word_count']}")
            print(f"Message: {row['message'][:200]}...")
            print("-" * 60)
    
    def url_domain_analysis(self):
        """Analyze most shared domains"""
        print("\n" + "=" * 60)
        print("MOST SHARED DOMAINS")
        print("=" * 60)
        
        url_pattern = r'https?://(?:www\.)?([^/\s]+)'
        domains = []
        
        for msg in self.df['message']:
            urls = re.findall(url_pattern, msg)
            domains.extend(urls)
        
        if domains:
            domain_counts = Counter(domains).most_common(15)
            for domain, count in domain_counts:
                bar = '█' * int(count / domain_counts[0][1] * 40)
                print(f"{domain[:35]:35s} | {bar} {count}")
        else:
            print("No URLs found in chat.")
    
    def sentiment_keywords(self):
        """Analyze positive and negative sentiment keywords"""
        print("\n" + "=" * 60)
        print("SENTIMENT KEYWORD ANALYSIS")
        print("=" * 60)
        
        positive_words = {'love', 'great', 'awesome', 'good', 'nice', 'happy', 'thanks', 
                         'thank', 'best', 'excellent', 'amazing', 'wonderful', 'fantastic',
                         'perfect', 'glad', 'congrats', 'congratulations', 'lol', 'haha'}
        
        negative_words = {'hate', 'bad', 'terrible', 'worst', 'angry', 'sad', 'sorry',
                         'problem', 'issue', 'difficult', 'hard', 'annoying', 'frustrated',
                         'stupid', 'damn', 'wrong', 'mistake'}
        
        positive_count = 0
        negative_count = 0
        
        for msg in self.df['message'].str.lower():
            words = set(re.findall(r'\b[a-zA-Z]+\b', msg))
            positive_count += len(words.intersection(positive_words))
            negative_count += len(words.intersection(negative_words))
        
        total = positive_count + negative_count
        if total > 0:
            print(f"Positive Keywords: {positive_count} ({positive_count/total*100:.2f}%)")
            print(f"Negative Keywords: {negative_count} ({negative_count/total*100:.2f}%)")
            
            pos_bar = '█' * int(positive_count / total * 50)
            neg_bar = '█' * int(negative_count / total * 50)
            
            print(f"\nPositive | {pos_bar}")
            print(f"Negative | {neg_bar}")
        else:
            print("No sentiment keywords found.")
    
    def author_response_rate(self):
        """Calculate how often each author responds to others"""
        print("\n" + "=" * 60)
        print("AUTHOR RESPONSE RATE")
        print("=" * 60)
        
        author_messages = {}
        author_responses = {}
        
        for author in self.df['author'].unique():
            author_messages[author] = 0
            author_responses[author] = 0
        
        for i in range(len(self.df)):
            author = self.df.iloc[i]['author']
            author_messages[author] += 1
            
            if i > 0 and self.df.iloc[i]['author'] != self.df.iloc[i-1]['author']:
                time_diff = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 60
                if time_diff < 15:  # Response within 15 minutes
                    author_responses[author] += 1
        
        print(f"{'Author':<30s} | {'Response Rate':<15s} | Total Msgs")
        print("-" * 60)
        
        for author in sorted(author_messages.keys(), key=lambda x: author_messages[x], reverse=True)[:15]:
            if author_messages[author] > 0:
                response_rate = author_responses[author] / author_messages[author] * 100
                bar = '█' * int(response_rate / 100 * 20)
                print(f"{author[:30]:<30s} | {bar:<15s} {response_rate:5.1f}% | {author_messages[author]}")
    
    def conversation_length_analysis(self):
        """Analyze conversation burst lengths"""
        print("\n" + "=" * 60)
        print("CONVERSATION BURST ANALYSIS")
        print("=" * 60)
        
        bursts = []
        current_burst = 1
        
        for i in range(1, len(self.df)):
            time_diff = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 60
            if time_diff < 5:  # Messages within 5 minutes = same burst
                current_burst += 1
            else:
                if current_burst > 1:
                    bursts.append(current_burst)
                current_burst = 1
        
        if bursts:
            print(f"Total Conversation Bursts: {len(bursts)}")
            print(f"Average Messages per Burst: {sum(bursts) / len(bursts):.2f}")
            print(f"Longest Burst: {max(bursts)} messages")
            print(f"Median Burst Length: {sorted(bursts)[len(bursts)//2]}")
        else:
            print("No conversation bursts detected.")
    
    def silence_periods(self):
        """Find longest periods of silence"""
        print("\n" + "=" * 60)
        print("TOP 10 LONGEST SILENCE PERIODS")
        print("=" * 60)
        
        gaps = []
        for i in range(1, len(self.df)):
            gap = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 3600
            if gap > 1:  # More than 1 hour
                gaps.append({
                    'start': self.df.iloc[i-1]['datetime'],
                    'end': self.df.iloc[i]['datetime'],
                    'hours': gap
                })
        
        gaps.sort(key=lambda x: x['hours'], reverse=True)
        
        for idx, gap in enumerate(gaps[:10], 1):
            days = gap['hours'] / 24
            print(f"{idx}. {gap['start'].date()} to {gap['end'].date()} - {days:.1f} days ({gap['hours']:.1f} hours)")
    
    def unique_participant_daily(self):
        """Track unique participants per day"""
        print("\n" + "=" * 60)
        print("DAILY UNIQUE PARTICIPANT ANALYSIS")
        print("=" * 60)
        
        daily_unique = self.df.groupby('date_only')['author'].nunique()
        
        print(f"Average Unique Participants per Day: {daily_unique.mean():.2f}")
        print(f"Maximum Active Participants in a Day: {daily_unique.max()}")
        print(f"Minimum Active Participants in a Day: {daily_unique.min()}")
        
        print(f"\nDays with Most Participants:")
        for date, count in daily_unique.nlargest(5).items():
            print(f"{date} : {count} participants")
    
    def early_bird_analysis(self):
        """Find who chats early morning"""
        print("\n" + "=" * 60)
        print("EARLY BIRD ANALYSIS (5 AM - 8 AM)")
        print("=" * 60)
        
        morning_messages = self.df[(self.df['hour'] >= 5) & (self.df['hour'] < 8)]
        
        if len(morning_messages) > 0:
            print(f"Total Morning Messages: {len(morning_messages)}")
            print(f"Percentage of Total: {len(morning_messages) / len(self.df) * 100:.2f}%")
            print(f"\nEarly Birds:")
            
            early_birds = morning_messages.groupby('author').size().sort_values(ascending=False).head(10)
            for author, count in early_birds.items():
                bar = '█' * int(count / early_birds.max() * 40)
                print(f"{author[:25]:25s} | {bar} {count}")
        else:
            print("No early morning messages found.")
    
    def busy_hour_by_author(self):
        """Find each author's most active hour"""
        print("\n" + "=" * 60)
        print("EACH AUTHOR'S BUSIEST HOUR")
        print("=" * 60)
        
        top_authors = self.df['author'].value_counts().head(10).index
        
        for author in top_authors:
            author_df = self.df[self.df['author'] == author]
            busiest_hour = author_df['hour'].mode()[0]
            hour_count = (author_df['hour'] == busiest_hour).sum()
            print(f"{author[:30]:30s} | {busiest_hour:02d}:00 ({hour_count} msgs)")
    
    def message_type_analysis(self):
        """Categorize messages by type"""
        print("\n" + "=" * 60)
        print("MESSAGE TYPE BREAKDOWN")
        print("=" * 60)
        
        media = self.df[self.df['message'].str.contains('<Media omitted>|image omitted|video omitted|audio omitted|sticker omitted', case=False, na=False)].shape[0]
        
        links = self.df[self.df['message'].str.contains('http', case=False, na=False) & 
                       ~self.df['message'].str.contains('<Media omitted>', case=False, na=False)].shape[0]
        
        deleted = self.df[self.df['message'].str.contains('deleted|This message was deleted', case=False, na=False)].shape[0]
        
        questions = self.df[self.df['message'].str.contains(r'\?', na=False)].shape[0]
        
        short_msgs = self.df[self.df['word_count'] <= 3].shape[0]
        
        long_msgs = self.df[self.df['word_count'] >= 50].shape[0]
        
        total = len(self.df)
        
        print(f"Media Messages:      {media:6d} ({media/total*100:5.2f}%)")
        print(f"Links Shared:        {links:6d} ({links/total*100:5.2f}%)")
        print(f"Deleted Messages:    {deleted:6d} ({deleted/total*100:5.2f}%)")
        print(f"Questions:           {questions:6d} ({questions/total*100:5.2f}%)")
        print(f"Short (≤3 words):    {short_msgs:6d} ({short_msgs/total*100:5.2f}%)")
        print(f"Long (≥50 words):    {long_msgs:6d} ({long_msgs/total*100:5.2f}%)")
    
    def author_consistency(self):
        """Measure how consistently each author participates"""
        print("\n" + "=" * 60)
        print("AUTHOR CONSISTENCY SCORE")
        print("=" * 60)
        
        total_days = (self.df['datetime'].max() - self.df['datetime'].min()).days
        
        print(f"{'Author':<30s} | Days Active | Consistency")
        print("-" * 60)
        
        for author in self.df['author'].value_counts().head(15).index:
            author_days = self.df[self.df['author'] == author]['date_only'].nunique()
            consistency = author_days / total_days * 100 if total_days > 0 else 0
            bar = '█' * int(consistency / 100 * 30)
            print(f"{author[:30]:<30s} | {author_days:4d}/{total_days:4d}   | {bar} {consistency:.1f}%")
    
    def peak_activity_finder(self):
        """Find the single most active hour-day combination"""
        print("\n" + "=" * 60)
        print("PEAK ACTIVITY TIMES")
        print("=" * 60)
        
        self.df['hour_day'] = self.df['day_of_week'] + ' ' + self.df['hour'].astype(str) + ':00'
        peak_times = self.df['hour_day'].value_counts().head(10)
        
        print("Top 10 Busiest Hour-Day Combinations:")
        for time_slot, count in peak_times.items():
            bar = '█' * int(count / peak_times.max() * 40)
            print(f"{time_slot:20s} | {bar} {count}")
    
    def reply_speed_by_author(self):
        """Calculate average reply speed for each author"""
        print("\n" + "=" * 60)
        print("AVERAGE REPLY SPEED BY AUTHOR")
        print("=" * 60)
        
        reply_times = {author: [] for author in self.df['author'].unique()}
        
        for i in range(1, len(self.df)):
            if self.df.iloc[i]['author'] != self.df.iloc[i-1]['author']:
                time_diff = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 60
                if time_diff < 60:  # Only consider replies within 1 hour
                    reply_times[self.df.iloc[i]['author']].append(time_diff)
        
        avg_reply = [(author, sum(times)/len(times)) for author, times in reply_times.items() if len(times) > 5]
        avg_reply.sort(key=lambda x: x[1])
        
        print("Fastest Responders (avg minutes):")
        for author, avg_time in avg_reply[:15]:
            bar = '█' * int((60 - min(avg_time, 60)) / 60 * 30)
            print(f"{author[:30]:30s} | {bar} {avg_time:.2f} min")
    
    def word_cloud_data(self, top_n=50):
        """Export data for word cloud generation"""
        print(f"\n" + "=" * 60)
        print(f"TOP {top_n} WORDS FOR WORD CLOUD")
        print("=" * 60)
        
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'is', 'was', 'are', 'be', 'been', 'have', 'has', 'had',
                      'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                      'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that', 'these', 
                      'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'me', 'him',
                      'us', 'them', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}
        
        all_words = []
        for msg in self.df['message']:
            if not any(x in msg.lower() for x in ['<media omitted>', 'image omitted', 'video omitted']):
                words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
                all_words.extend([w for w in words if w not in stop_words])
        
        word_freq = Counter(all_words).most_common(top_n)
        
        print("Word:Frequency pairs (for word cloud):")
        for word, count in word_freq:
            print(f"{word}:{count}", end="  ")
        print("\n")
    
    def who_talks_to_whom(self):
        """Analyze direct reply patterns between specific users"""
        print("\n" + "=" * 60)
        print("WHO TALKS TO WHOM MOST (Direct Replies)")
        print("=" * 60)
        
        reply_pairs = []
        for i in range(1, len(self.df)):
            if self.df.iloc[i]['author'] != self.df.iloc[i-1]['author']:
                time_diff = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 60
                if time_diff < 5:  # Quick reply within 5 minutes
                    reply_pairs.append((self.df.iloc[i-1]['author'], self.df.iloc[i]['author']))
        
        if reply_pairs:
            pair_counts = Counter(reply_pairs).most_common(20)
            for (from_user, to_user), count in pair_counts:
                print(f"{from_user[:20]:20s} ➜ {to_user[:20]:20s} : {count} times")
    
    def monologue_detection(self):
        """Find longest message monologues (consecutive messages by same person)"""
        print("\n" + "=" * 60)
        print("LONGEST MONOLOGUES (Consecutive Messages)")
        print("=" * 60)
        
        monologues = []
        current_author = self.df.iloc[0]['author']
        current_count = 1
        start_idx = 0
        
        for i in range(1, len(self.df)):
            if self.df.iloc[i]['author'] == current_author:
                current_count += 1
            else:
                if current_count >= 5:
                    monologues.append({
                        'author': current_author,
                        'count': current_count,
                        'start_time': self.df.iloc[start_idx]['datetime']
                    })
                current_author = self.df.iloc[i]['author']
                current_count = 1
                start_idx = i
        
        monologues.sort(key=lambda x: x['count'], reverse=True)
        
        for idx, mono in enumerate(monologues[:10], 1):
            print(f"{idx}. {mono['author'][:25]:25s} - {mono['count']} msgs in a row on {mono['start_time'].date()}")
    
    def mention_analysis(self):
        """Analyze @mentions in messages"""
        print("\n" + "=" * 60)
        print("@MENTION ANALYSIS")
        print("=" * 60)
        
        mentions = []
        for msg in self.df['message']:
            found = re.findall(r'@(\w+)', msg)
            mentions.extend(found)
        
        if mentions:
            mention_counts = Counter(mentions).most_common(15)
            print(f"Total @mentions: {len(mentions)}")
            print(f"\nMost Mentioned Users:")
            for user, count in mention_counts:
                bar = '█' * int(count / mention_counts[0][1] * 40)
                print(f"@{user[:25]:25s} | {bar} {count}")
        else:
            print("No @mentions found in chat.")
    
    def hashtag_analysis(self):
        """Analyze hashtags used"""
        print("\n" + "=" * 60)
        print("HASHTAG ANALYSIS")
        print("=" * 60)
        
        hashtags = []
        for msg in self.df['message']:
            found = re.findall(r'#(\w+)', msg)
            hashtags.extend([h.lower() for h in found])
        
        if hashtags:
            tag_counts = Counter(hashtags).most_common(15)
            print(f"Total Hashtags: {len(hashtags)}")
            print(f"\nMost Used Hashtags:")
            for tag, count in tag_counts:
                bar = '█' * int(count / tag_counts[0][1] * 40)
                print(f"#{tag[:25]:25s} | {bar} {count}")
        else:
            print("No hashtags found in chat.")
    
    def caps_lock_analysis(self):
        """Find who uses CAPS LOCK most"""
        print("\n" + "=" * 60)
        print("CAPS LOCK USAGE (SHOUTING ANALYSIS)")
        print("=" * 60)
        
        caps_by_author = {}
        
        for idx, row in self.df.iterrows():
            author = row['author']
            msg = row['message']
            
            # Count words in all caps (at least 4 letters)
            caps_words = re.findall(r'\b[A-Z]{4,}\b', msg)
            
            if author not in caps_by_author:
                caps_by_author[author] = 0
            caps_by_author[author] += len(caps_words)
        
        sorted_caps = sorted(caps_by_author.items(), key=lambda x: x[1], reverse=True)[:15]
        
        if sorted_caps[0][1] > 0:
            print("Top CAPS Users:")
            for author, count in sorted_caps:
                if count > 0:
                    bar = '█' * int(count / sorted_caps[0][1] * 40)
                    print(f"{author[:25]:25s} | {bar} {count}")
        else:
            print("No significant CAPS usage found.")
    
    def laugh_analysis(self):
        """Analyze different types of laughter"""
        print("\n" + "=" * 60)
        print("LAUGHTER ANALYSIS")
        print("=" * 60)
        
        laugh_patterns = {
            'haha': r'\bhaha+\b',
            'lol': r'\blol+\b',
            'lmao': r'\blmao+\b',
            'rofl': r'\brofl+\b',
            'hehe': r'\bhehe+\b',
            '😂': r'😂',
            '🤣': r'🤣',
            '😆': r'😆'
        }
        
        laugh_counts = {}
        for laugh_type, pattern in laugh_patterns.items():
            count = self.df['message'].str.lower().str.contains(pattern, regex=True, na=False).sum()
            if count > 0:
                laugh_counts[laugh_type] = count
        
        if laugh_counts:
            sorted_laughs = sorted(laugh_counts.items(), key=lambda x: x[1], reverse=True)
            print(f"Total Laughter Expressions: {sum(laugh_counts.values())}")
            print(f"\nLaughter Types:")
            for laugh, count in sorted_laughs:
                bar = '█' * int(count / sorted_laughs[0][1] * 40)
                print(f"{laugh:10s} | {bar} {count}")
        else:
            print("No laughter expressions found.")
    
    def politeness_analysis(self):
        """Analyze politeness indicators"""
        print("\n" + "=" * 60)
        print("POLITENESS ANALYSIS")
        print("=" * 60)
        
        polite_words = {
            'please': 0, 'thanks': 0, 'thank you': 0, 'sorry': 0,
            'excuse me': 0, 'appreciate': 0, 'grateful': 0, 'welcome': 0
        }
        
        for msg in self.df['message'].str.lower():
            for word in polite_words.keys():
                if word in msg:
                    polite_words[word] += 1
        
        total_polite = sum(polite_words.values())
        if total_polite > 0:
            print(f"Total Polite Expressions: {total_polite}")
            print(f"Politeness Rate: {total_polite / len(self.df) * 100:.2f}% of messages")
            print(f"\nMost Used Polite Words:")
            for word, count in sorted(polite_words.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    bar = '█' * int(count / total_polite * 40)
                    print(f"{word:15s} | {bar} {count}")
        else:
            print("No politeness indicators found.")
    
    def punctuation_personality(self):
        """Analyze punctuation usage patterns"""
        print("\n" + "=" * 60)
        print("PUNCTUATION PERSONALITY")
        print("=" * 60)
        
        punct_analysis = {
            'exclamation': self.df['message'].str.count('!').sum(),
            'question': self.df['message'].str.count(r'\?').sum(),
            'ellipsis': self.df['message'].str.count(r'\.\.\.').sum(),
            'multiple_punct': self.df['message'].str.contains(r'[!?]{2,}', regex=True).sum()
        }
        
        total = sum(punct_analysis.values())
        if total > 0:
            print(f"Exclamation marks (!): {punct_analysis['exclamation']}")
            print(f"Question marks (?): {punct_analysis['question']}")
            print(f"Ellipsis (...): {punct_analysis['ellipsis']}")
            print(f"Multiple punctuation (!!?, ???): {punct_analysis['multiple_punct']}")
        else:
            print("No special punctuation patterns found.")
    
    def time_to_first_message(self):
        """Calculate how long it takes for first message of the day"""
        print("\n" + "=" * 60)
        print("DAILY FIRST MESSAGE TIMES")
        print("=" * 60)
        
        first_msgs = self.df.groupby('date_only')['hour'].min()
        
        hour_dist = Counter(first_msgs)
        
        print("Distribution of first message hours:")
        for hour in sorted(hour_dist.keys()):
            count = hour_dist[hour]
            bar = '█' * int(count / max(hour_dist.values()) * 40)
            print(f"{hour:02d}:00 | {bar} {count} days")
    
    def author_vocabulary_richness(self):
        """Measure vocabulary diversity per author"""
        print("\n" + "=" * 60)
        print("VOCABULARY RICHNESS (Unique Words per 100 Messages)")
        print("=" * 60)
        
        vocab_scores = {}
        
        for author in self.df['author'].value_counts().head(15).index:
            author_msgs = self.df[self.df['author'] == author]['message']
            all_words = []
            for msg in author_msgs:
                words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
                all_words.extend(words)
            
            if len(all_words) > 0:
                unique_words = len(set(all_words))
                total_words = len(all_words)
                richness = (unique_words / total_words) * 100
                vocab_scores[author] = richness
        
        sorted_vocab = sorted(vocab_scores.items(), key=lambda x: x[1], reverse=True)
        
        for author, score in sorted_vocab:
            bar = '█' * int(score / sorted_vocab[0][1] * 40)
            print(f"{author[:25]:25s} | {bar} {score:.1f}%")
    
    def forwarded_message_analysis(self):
        """Analyze forwarded messages"""
        print("\n" + "=" * 60)
        print("FORWARDED MESSAGE ANALYSIS")
        print("=" * 60)
        
        forwarded = self.df[self.df['message'].str.contains('forwarded', case=False, na=False)]
        
        if len(forwarded) > 0:
            print(f"Total Forwarded Messages: {len(forwarded)}")
            print(f"Percentage: {len(forwarded) / len(self.df) * 100:.2f}%")
            print(f"\nTop Forwarders:")
            
            forwarders = forwarded.groupby('author').size().sort_values(ascending=False).head(10)
            for author, count in forwarders.items():
                bar = '█' * int(count / forwarders.max() * 40)
                print(f"{author[:25]:25s} | {bar} {count}")
        else:
            print("No forwarded messages detected.")
    
    def conversation_initiator_by_time(self):
        """Who starts conversations at different times of day"""
        print("\n" + "=" * 60)
        print("CONVERSATION INITIATORS BY TIME OF DAY")
        print("=" * 60)
        
        time_periods = {
            'Morning (6-12)': (6, 12),
            'Afternoon (12-18)': (12, 18),
            'Evening (18-24)': (18, 24),
            'Night (0-6)': (0, 6)
        }
        
        for period, (start, end) in time_periods.items():
            print(f"\n{period}:")
            starters = []
            for i in range(1, len(self.df)):
                hour = self.df.iloc[i]['hour']
                if start <= hour < end:
                    time_gap = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 3600
                    if time_gap > 3:
                        starters.append(self.df.iloc[i]['author'])
            
            if starters:
                starter_counts = Counter(starters).most_common(5)
                for author, count in starter_counts:
                    print(f"  {author[:25]:25s} : {count}")
    
    def engagement_score(self):
        """Calculate engagement score for each author"""
        print("\n" + "=" * 60)
        print("ENGAGEMENT SCORE (Composite Metric)")
        print("=" * 60)
        
        scores = {}
        
        for author in self.df['author'].value_counts().head(15).index:
            author_df = self.df[self.df['author'] == author]
            
            # Metrics
            msg_count = len(author_df)
            avg_words = author_df['word_count'].mean()
            days_active = author_df['date_only'].nunique()
            
            # Simple engagement score
            engagement = (msg_count * 0.4) + (avg_words * 0.3) + (days_active * 0.3)
            scores[author] = engagement
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        print("Top Engaged Users:")
        for author, score in sorted_scores:
            bar = '█' * int(score / sorted_scores[0][1] * 40)
            print(f"{author[:25]:25s} | {bar} {score:.0f}")
    
    def seasonal_activity(self):
        """Analyze activity by season (if data spans multiple seasons)"""
        print("\n" + "=" * 60)
        print("SEASONAL ACTIVITY PATTERN")
        print("=" * 60)
        
        self.df['season'] = self.df['datetime'].dt.month.map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        seasonal = self.df.groupby('season').size()
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        
        for season in season_order:
            if season in seasonal.index:
                count = seasonal[season]
                bar = '█' * int(count / seasonal.max() * 50)
                print(f"{season:10s} | {bar} {count}")
    
    def reply_chain_depth(self):
        """Analyze depth of reply chains"""
        print("\n" + "=" * 60)
        print("REPLY CHAIN DEPTH ANALYSIS")
        print("=" * 60)
        
        chain_lengths = []
        current_chain = 1
        
        for i in range(1, len(self.df)):
            time_diff = (self.df.iloc[i]['datetime'] - self.df.iloc[i-1]['datetime']).total_seconds() / 60
            if time_diff < 2:  # Messages within 2 minutes
                current_chain += 1
            else:
                if current_chain > 2:
                    chain_lengths.append(current_chain)
                current_chain = 1
        
        if chain_lengths:
            print(f"Total Reply Chains: {len(chain_lengths)}")
            print(f"Average Chain Length: {sum(chain_lengths) / len(chain_lengths):.2f} messages")
            print(f"Longest Chain: {max(chain_lengths)} messages")
            print(f"Median Chain: {sorted(chain_lengths)[len(chain_lengths)//2]} messages")
        else:
            print("No significant reply chains detected.")
    
    def run_all_analyses(self):
        """Run all analyses"""
        self.basic_stats()
        self.author_stats()
        self.activity_by_time()
        self.activity_by_day()
        self.most_active_days()
        self.media_and_links()
        self.most_common_words()
        self.emoji_analysis()
        self.response_time_analysis()
        self.conversation_starters()
        self.message_length_analysis()
        self.deleted_messages_analysis()
        self.question_analysis()
        self.night_owl_analysis()
        self.ghost_analysis()
        self.monthly_trend()
        self.streak_analysis()
        self.author_interaction_matrix()
        self.weekend_vs_weekday()
        self.find_longest_messages()
        self.url_domain_analysis()
        self.sentiment_keywords()
        self.author_response_rate()
        self.conversation_length_analysis()
        self.silence_periods()
        self.unique_participant_daily()
        self.early_bird_analysis()
        self.busy_hour_by_author()
        self.message_type_analysis()
        self.author_consistency()
        self.peak_activity_finder()
        self.reply_speed_by_author()
        self.word_cloud_data()
        self.who_talks_to_whom()
        self.monologue_detection()
        self.mention_analysis()
        self.hashtag_analysis()
        self.caps_lock_analysis()
        self.laugh_analysis()
        self.politeness_analysis()
        self.punctuation_personality()
        self.time_to_first_message()
        self.author_vocabulary_richness()
        self.forwarded_message_analysis()
        self.conversation_initiator_by_time()
        self.engagement_score()
        self.seasonal_activity()
        self.reply_chain_depth()
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE - 54 ANALYSES PERFORMED!")
        print("=" * 60)

# Usage
if __name__ == "__main__":
    # Replace with your chat file path
    analyzer = WhatsAppAnalyzer('WhatsApp Chat.txt')
    analyzer.run_all_analyses()