# 🤖 ModBot - AI Agentic Discord Moderator

An intelligent Discord moderation bot powered by AI that automatically moderates messages using OpenAI's GPT models and LlamaIndex. The bot can warn, delete messages, or ban users based on configurable server rules.

## ✨ Features

- **AI-Powered Moderation**: Uses OpenAI's GPT models to intelligently analyze messages
- **Configurable Rules**: Update moderation rules on-the-fly using Discord commands
- **Progressive Warning System**: 3-strike warning system before automatic bans
- **Context-Aware**: Considers message context for better moderation decisions
- **Multiple Actions**: Supports OK, Delete, Warn, and Ban actions
- **Guild-Scoped**: Separate warning tracking per Discord server
- **Real-time Updates**: Update moderation rules without restarting the bot

## 🏗️ Architecture

```
ModBot/
├── main.py              # Main Discord bot entry point
├── agent/
│   ├── agent_service.py # AI moderation agent logic
│   └── test_agent.py    # Testing utilities
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment config
└── warnings.db         # SQLite database for warning tracking
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Discord Bot Token
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ModBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Enable the following bot permissions:
   - Send Messages
   - Manage Messages (for deleting messages)
   - Ban Members
   - Read Message History

### Bot Permissions

The bot requires these Discord permissions:
- `Send Messages` - To send moderation notifications
- `Manage Messages` - To delete violating messages
- `Ban Members` - To ban users who violate rules
- `Read Message History` - To access message context

## 📝 Usage

### Commands

- `!update_rules <rules_text>` - Update the moderation rules
  ```
  !update_rules No hate speech. No harassment. Be respectful. No spam.
  ```

### Moderation Actions

The AI agent can take the following actions:

- **OK** - Message is acceptable, no action taken
- **Delete** - Message is deleted immediately
- **Warn** - User receives a warning (counts toward 3-strike system)
- **Ban** - User is banned immediately

### Warning System

- Users get warnings for minor violations
- After 3 warnings, users are automatically banned
- Warning counts are tracked per server (guild)
- Warning counts reset after a ban

## 🤖 AI Agent Details

### ModerationAgent Class

The core AI moderation logic is handled by the `ModerationAgent` class in `agent/agent_service.py`:

```python
from agent.agent_service import ModerationAgent

# Create agent with custom rules
agent = ModerationAgent(server_rules="No hate speech. Be respectful.")

# Moderate a message
action = agent.moderate_message("Hello world!")
```

### Features

- **ReAct Agent**: Uses LlamaIndex's ReAct agent for reasoning
- **Vector Search**: Rules are indexed for semantic search
- **Context Awareness**: Considers previous messages for context
- **Fallback Logic**: Invalid responses default to "OK"
- **Dynamic Rules**: Update rules without restarting

### Default Rules

If no custom rules are provided, the bot uses these default rules:
- Hate speech → Ban
- Harassment → Ban
- Spam → Ban
- Mild insults → Delete
- Repeated minor violations → Warn
- Normal messages → OK

## 🗄️ Database

The bot uses SQLite (`warnings.db`) to track user warnings:

```sql
CREATE TABLE warnings (
    user_id  TEXT NOT NULL,
    guild_id TEXT NOT NULL,
    count    INTEGER NOT NULL,
    PRIMARY KEY (user_id, guild_id)
);
```

- **user_id**: Discord user ID
- **guild_id**: Discord server (guild) ID
- **count**: Number of warnings (1-3)

## 🧪 Testing

Run the test agent to verify moderation logic:

```bash
cd agent
python test_agent.py
```

This will test the moderation agent with example messages and rules.

## 🚀 Deployment

### Heroku Deployment

The project includes a `Procfile` for easy Heroku deployment:

1. Create a Heroku app
2. Set environment variables in Heroku dashboard:
   - `DISCORD_TOKEN`
   - `OPENAI_API_KEY`
3. Deploy using Heroku CLI or GitHub integration

### Local Development

For local development, ensure you have:
- Python virtual environment activated
- All dependencies installed
- Environment variables set in `.env` file

## 🔒 Security Considerations

- **API Key Protection**: Never commit API keys to version control
- **Bot Permissions**: Use minimal required permissions
- **Rate Limiting**: Consider implementing rate limiting for rule updates
- **Logging**: Monitor bot actions for abuse

## 📊 Monitoring

The bot provides console logging for:
- Message processing
- Moderation decisions
- Warning increments
- Ban actions
- Rule updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the console logs for error messages
2. Verify your API keys are correct
3. Ensure the bot has proper Discord permissions
4. Check that all dependencies are installed

## 🔮 Future Enhancements

Potential improvements:
- [ ] Web dashboard for rule management
- [ ] Advanced analytics and reporting
- [ ] Custom moderation levels per channel
- [ ] Integration with external moderation APIs
- [ ] Appeal system for banned users
- [ ] Automated rule learning from moderator actions 