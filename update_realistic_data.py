#!/usr/bin/env python3
"""
Update BBS Forum with realistic data.
Updates usernames, post titles/content, and reply content while preserving IDs and relationships.
"""

import random
from app import create_app, db
from app.models import User, Post, Reply, Category

# Realistic first names
FIRST_NAMES = [
    'Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn',
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'William', 'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia', 'Lucas',
    'Harper', 'Henry', 'Evelyn', 'Alexander', 'Abigail', 'Michael', 'Emily', 'Daniel',
    'Elizabeth', 'Matthew', 'Sofia', 'David', 'Ella', 'Joseph', 'Madison', 'Samuel',
    'Scarlett', 'Jackson', 'Victoria', 'Sebastian', 'Aria', 'Jack', 'Grace', 'Aiden',
    'Chloe', 'Owen', 'Camila', 'Dylan', 'Penelope', 'Luke', 'Riley', 'Gabriel',
    'Layla', 'Anthony', 'Lillian', 'Isaac', 'Nora', 'Grayson', 'Zoey', 'Jayden',
    'Mila', 'Lincoln', 'Aubrey', 'Levi', 'Hannah', 'Theodore', 'Lily', 'Mateo',
    'Addison', 'Leo', 'Eleanor', 'Wyatt', 'Natalie', 'John', 'Luna', 'Asher'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
    'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
    'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
    'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
    'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
    'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
    'Cook', 'Rogers', 'Morgan', 'Peterson', 'Cooper', 'Reed', 'Bailey', 'Bell',
    'Howard', 'Ward', 'Cox', 'Richardson', 'Wood', 'Watson', 'Brooks', 'Bennett'
]

# Category-specific post content generators
def generate_general_post(title):
    """Generate general discussion post content"""
    templates = [
        f"I've been thinking about this topic for a while now and wanted to get everyone's perspective. {title}\n\nFrom what I've observed, there are multiple viewpoints on this matter. Some people believe one thing, while others have completely different experiences. I'm curious to hear what this community thinks.\n\nWhat are your thoughts? Has anyone else encountered similar situations? I'd love to hear your stories and insights.",

        f"Hey everyone! I wanted to start a discussion about something that's been on my mind lately.\n\n{title}\n\nI think this is an interesting topic that affects many of us in different ways. I've noticed various approaches people take, and I'm curious about what works best for different situations.\n\nLooking forward to hearing your perspectives and experiences!",

        f"This might be a bit of an unusual question, but I figured this would be the perfect place to ask.\n\n{title}\n\nI've been doing some research on my own, but I'd really value the community's input on this. There seem to be pros and cons to different approaches, and I'm trying to figure out what makes the most sense.\n\nAny advice or shared experiences would be greatly appreciated!"
    ]
    return random.choice(templates)

def generate_tech_post(title):
    """Generate technology post content"""
    templates = [
        f"I've been working with various tech solutions lately and ran into an interesting situation.\n\n{title}\n\nI've tried a few different approaches, but I'm not entirely satisfied with the results. The performance seems okay, but I feel like there might be better options out there that I'm not aware of.\n\nHas anyone dealt with something similar? What tools or methods did you find most effective? I'm open to suggestions and would love to hear about your experiences.",

        f"Quick question for the tech-savvy folks here:\n\n{title}\n\nI've been reading various articles and watching tutorials, but I'm getting conflicting information. Some sources recommend one approach, while others suggest something completely different.\n\nWhat's been your experience? Are there any best practices I should be aware of? Any pitfalls to avoid?",

        f"I need some advice from the community on a tech-related matter.\n\n{title}\n\nI'm currently evaluating different options and trying to determine the best path forward. Budget is a consideration, but I'm more focused on reliability and long-term viability.\n\nWould love to hear recommendations from people who have actually used these solutions in real-world scenarios. What worked for you?"
    ]
    return random.choice(templates)

def generate_programming_post(title):
    """Generate programming post content"""
    templates = [
        f"I'm working on a project and hit a roadblock that I could use some help with.\n\n{title}\n\nI've been coding for a while now, but this particular challenge has me stumped. I've tried several different approaches and looked through documentation, but I'm not getting the results I expected.\n\nThe code runs without errors, but the behavior isn't quite right. Has anyone encountered something similar? I'd appreciate any insights or suggestions on how to approach this problem.",

        f"Developer question here:\n\n{title}\n\nI'm trying to decide between different implementation approaches and wanted to get input from more experienced developers. Each option has its trade-offs, and I'm not sure which would be best for my use case.\n\nWhat factors do you typically consider when making these kinds of decisions? Are there any gotchas I should be aware of?",

        f"Looking for some coding advice from the community.\n\n{title}\n\nI've been working on this for a few days now and I feel like I'm missing something fundamental. The logic seems sound, but the implementation is proving more challenging than I anticipated.\n\nHas anyone solved a similar problem before? What approach did you take? Any libraries or frameworks that might help?"
    ]
    return random.choice(templates)

def generate_gaming_post(title):
    """Generate gaming post content"""
    templates = [
        f"Gaming discussion time!\n\n{title}\n\nI've been playing for a while now and wanted to share my thoughts with the community. The experience has been interesting so far, with both highs and lows.\n\nI'm curious about other players' experiences. What strategies have you found effective? Any tips for someone looking to improve their gameplay?\n\nLet's discuss!",

        f"Hey fellow gamers!\n\n{title}\n\nI just finished a long gaming session and I'm still processing everything. There were some really memorable moments, but also some frustrating parts that I'm trying to figure out.\n\nWhat's been your experience? How do you deal with challenging sections? Any recommendations for making the most of the game?",

        f"Quick gaming question:\n\n{title}\n\nI've been following this for a while and finally decided to dive in. So far, it's been quite an adventure. The mechanics are interesting, though there's definitely a learning curve.\n\nFor those who are more experienced, what advice would you give to someone just starting out? What do you wish you'd known when you first began?"
    ]
    return random.choice(templates)

def generate_science_post(title):
    """Generate science/education post content"""
    templates = [
        f"I've been reading about this topic recently and found it fascinating.\n\n{title}\n\nThe more I learn, the more questions I have. The subject is deeper and more complex than I initially realized, with many interconnected concepts that build on each other.\n\nI'm trying to develop a better understanding of the fundamentals. Does anyone have good resources they'd recommend? Or insights from their own learning journey?",

        f"Educational discussion:\n\n{title}\n\nI've been studying this area for a while now, and I'm at the point where I'm trying to connect theoretical knowledge with practical applications. It's one thing to understand concepts in abstract, but quite another to see how they work in real situations.\n\nHas anyone found effective ways to bridge this gap? What learning methods have worked best for you?",

        f"Science question for the community:\n\n{title}\n\nI came across this topic while researching something else, and it sparked my curiosity. There seems to be a lot of interesting research in this area, though some of it is quite technical and challenging to parse.\n\nFor those familiar with this field, what are the key concepts I should focus on? Any good starting points for deeper exploration?"
    ]
    return random.choice(templates)

def generate_entertainment_post(title):
    """Generate entertainment post content"""
    templates = [
        f"I just experienced something I need to talk about!\n\n{title}\n\nWithout spoiling anything for those who haven't seen/heard/read it yet, I'll just say that it was quite an experience. There were moments that really stood out, and I'm still thinking about certain aspects days later.\n\nFor those who have experienced it, what did you think? I'd love to discuss specific elements (with proper spoiler warnings, of course).",

        f"Entertainment recommendation request:\n\n{title}\n\nI'm looking for suggestions from people with similar tastes. I enjoy things that are well-crafted and engaging, with depth beyond surface-level entertainment.\n\nWhat have you discovered recently that you'd recommend? I'm open to different genres and styles, as long as it's quality content.",

        f"Let's discuss:\n\n{title}\n\nI've been thinking about this lately and wanted to hear other perspectives. Entertainment is so subjective, and what resonates with one person might not work for another.\n\nWhat's your take on this? What factors do you consider when evaluating entertainment? Are there particular elements that are most important to you?"
    ]
    return random.choice(templates)

def generate_sports_post(title):
    """Generate sports/fitness post content"""
    templates = [
        f"Fitness journey update:\n\n{title}\n\nI've been working on this for a while now and wanted to share my progress and get some advice from the community. There have been some successes, but also challenges that I'm trying to work through.\n\nWhat's been your experience with similar goals? Any tips that helped you stay motivated and consistent? I'd appreciate any insights!",

        f"Sports discussion:\n\n{title}\n\nI've been following this closely and have some thoughts I wanted to share. The situation is interesting from multiple angles - performance, strategy, and broader implications.\n\nWhat's your analysis? I'm curious to hear different perspectives on how this might play out.",

        f"Looking for advice:\n\n{title}\n\nI'm trying to improve in this area and could use some guidance from more experienced people. I've done some research, but there's a lot of conflicting information out there.\n\nWhat approach has worked best for you? Any common mistakes I should avoid? What would you recommend for someone at my level?"
    ]
    return random.choice(templates)

def generate_travel_post(title):
    """Generate travel/lifestyle post content"""
    templates = [
        f"Travel planning question:\n\n{title}\n\nI'm in the early stages of planning and trying to gather information from people who have actually been there or done this. Online reviews are helpful, but I trust personal recommendations from real travelers more.\n\nWhat was your experience like? Any must-see/must-do recommendations? Things to avoid? Budget tips?\n\nI'd love to hear your stories and advice!",

        f"Lifestyle discussion:\n\n{title}\n\nI've been thinking about making some changes in this area and wanted to get input from the community. It's always helpful to hear from people who have gone through similar transitions.\n\nWhat challenges did you face? What worked well? What do you wish you'd done differently? Any advice for someone considering this?",

        f"Hey everyone!\n\n{title}\n\nI'm researching options and trying to make an informed decision. There are so many possibilities that it's a bit overwhelming. I'm looking for practical advice from people with firsthand experience.\n\nWhat factors did you consider? How did you narrow down your choices? What ultimately made the difference in your decision?"
    ]
    return random.choice(templates)

def generate_news_post(title):
    """Generate news/current events post content"""
    templates = [
        f"I wanted to start a discussion about something that's been in the news lately.\n\n{title}\n\nThis seems like an important topic that affects many people. I've been following the coverage from various sources, and there are clearly multiple perspectives on the situation.\n\nWhat's your take on this? I'm interested in hearing thoughtful analysis from different viewpoints. Let's keep the discussion respectful and focused on understanding the issues.",

        f"Current events discussion:\n\n{title}\n\nI've been reading about this and wanted to get the community's thoughts. The situation is complex, with many factors at play. It's not a simple issue with easy answers.\n\nWhat aspects do you think are most important to consider? How do you see this developing? I'm curious about informed perspectives on this.",

        f"This topic has been on my mind lately:\n\n{title}\n\nI think it's worth having a thoughtful conversation about this. There are implications that go beyond the immediate situation, and it's helpful to think through the broader context.\n\nWhat information should people be aware of? What questions should we be asking? Let's have a constructive discussion about this."
    ]
    return random.choice(templates)

def generate_offtopic_post(title):
    """Generate off-topic post content"""
    templates = [
        f"Random thought of the day:\n\n{title}\n\nThis doesn't really fit into any specific category, but I figured someone here might find it interesting or have thoughts on it. Sometimes the best discussions come from unexpected topics.\n\nAnyone else ever think about this? Am I the only one, or is this something others have considered too?",

        f"Just curious:\n\n{title}\n\nI know this is a bit random, but I'm genuinely curious about people's perspectives on this. It came up in a conversation recently and I realized I don't have a good answer.\n\nWhat do you all think? Is there a consensus on this, or is it one of those things where everyone has their own take?",

        f"Off-topic question:\n\n{title}\n\nI've been wondering about this for a while and figured this would be a good place to ask. It's not urgent or particularly important, just something that's been on my mind.\n\nDoes anyone have insights or experiences related to this? I'd be interested to hear different viewpoints!"
    ]
    return random.choice(templates)

# Post title templates by category
POST_TITLE_TEMPLATES = {
    'General Discussion': [
        "What's your opinion on {}?",
        "Can we talk about {}?",
        "Thoughts on {} in 2026?",
        "Discussion: {} - where do you stand?",
        "Help me understand {}",
        "Is {} really worth it?",
        "Why is {} so controversial?",
        "The truth about {}",
        "My experience with {}",
        "Does anyone else feel this way about {}?",
        "Unpopular opinion about {}",
        "Let's discuss {} honestly",
        "What's the deal with {}?",
        "Confused about {}",
        "Anyone else wondering about {}?"
    ],
    'Technology': [
        "Best {} for 2026?",
        "Is {} still relevant?",
        "Switching from {} - need advice",
        "{} vs {} - which should I choose?",
        "Problems with {} - solutions?",
        "New to {} - where to start?",
        "{} recommendations needed",
        "Is {} worth the upgrade?",
        "Disappointed with {} - alternatives?",
        "How to optimize {}?",
        "{} not working as expected",
        "Future of {}?",
        "Understanding {} better",
        "Best practices for {}",
        "Migrating to {} - tips?"
    ],
    'Programming & Development': [
        "Help with {} implementation",
        "Best way to handle {} in {}?",
        "{} performance issues",
        "Learning {} - resource recommendations",
        "Debug help: {} not working",
        "{} vs {} for this use case?",
        "Architecture advice for {}",
        "Testing strategies for {}",
        "Deploying {} - best practices?",
        "Security concerns with {}",
        "{} integration challenges",
        "Optimizing {} code",
        "Understanding {} patterns",
        "{} framework comparison",
        "API design for {}"
    ],
    'Gaming': [
        "Just finished {} - thoughts?",
        "Tips for {} gameplay?",
        "Is {} worth buying?",
        "Stuck on {} - need help",
        "Best {} build/strategy?",
        "{} vs {} - which is better?",
        "Multiplayer {} experience",
        "Story discussion: {}",
        "Performance issues with {}",
        "Hidden gems like {}?",
        "{} community thoughts",
        "Returning to {} after break",
        "New to {} - beginner advice?",
        "{} update impressions",
        "Favorite {} moments"
    ],
    'Science & Education': [
        "Explaining {} simply",
        "Learning {} - where to start?",
        "Interesting facts about {}",
        "Understanding {} better",
        "Resources for studying {}",
        "Recent developments in {}",
        "How does {} actually work?",
        "Common misconceptions about {}",
        "Practical applications of {}",
        "Teaching {} effectively",
        "{} for beginners",
        "Deep dive into {}",
        "Questions about {}",
        "Fascinating {} research",
        "Career in {} - advice?"
    ],
    'Entertainment & Media': [
        "Just watched {} - discussion",
        "Recommendations similar to {}?",
        "Thoughts on latest {}?",
        "Underrated {} worth checking out",
        "Disappointed by {}",
        "Plot holes in {}?",
        "Best {} of 2026 so far?",
        "Rewatching {} - new perspective",
        "Hidden meanings in {}?",
        "Soundtrack appreciation: {}",
        "Character analysis: {}",
        "Ending of {} - your interpretation?",
        "Comparing {} adaptations",
        "Behind the scenes: {}",
        "Why {} is so popular"
    ],
    'Sports & Fitness': [
        "Training advice for {}",
        "Progress update: {}",
        "Injury prevention for {}",
        "Nutrition tips for {}?",
        "Equipment recommendations: {}",
        "Beginner {} routine?",
        "Plateau with {} - help!",
        "Recovery strategies for {}",
        "Form check: {}",
        "Motivation for {}",
        "{} competition preparation",
        "Home workout for {}",
        "Professional {} analysis",
        "Team {} performance discussion",
        "Upcoming {} season predictions"
    ],
    'Travel & Lifestyle': [
        "Planning trip to {} - advice?",
        "Budget travel to {}",
        "Hidden gems in {}",
        "Is {} overrated?",
        "Best time to visit {}?",
        "Solo travel to {} - safe?",
        "Food recommendations in {}",
        "Accommodation tips for {}",
        "Day trips from {}",
        "Cultural experiences in {}",
        "Photography spots in {}",
        "Family-friendly {} activities",
        "Weekend getaway to {}",
        "Living in {} - what's it like?",
        "Sustainable travel to {}"
    ],
    'News & Current Events': [
        "Discussion: recent {} developments",
        "Impact of {} on {}",
        "Analysis: {} situation",
        "Understanding {} context",
        "Implications of {}",
        "Perspectives on {}",
        "Following {} closely",
        "What's happening with {}?",
        "Fact-checking {} claims",
        "Historical context for {}",
        "Expert opinions on {}",
        "Community response to {}",
        "Long-term effects of {}",
        "Comparing {} approaches",
        "Updates on {} situation"
    ],
    'Off-Topic': [
        "Random: {} thoughts",
        "Shower thought about {}",
        "DAE {} or just me?",
        "Weird question about {}",
        "Fun fact: {}",
        "Life hack for {}",
        "Nostalgia: {}",
        "Confession: {}",
        "Pet peeve: {}",
        "Appreciation post for {}",
        "Rant: {}",
        "TIL about {}",
        "Change my mind: {}",
        "Hot take on {}",
        "Who else {}?"
    ]
}

# Topic words for title generation
TOPIC_WORDS = {
    'General Discussion': [
        'social media habits', 'work-life balance', 'modern communication',
        'online privacy', 'personal growth', 'time management', 'decision making',
        'relationships', 'career changes', 'life priorities', 'daily routines',
        'productivity', 'mental health', 'learning new skills', 'hobbies'
    ],
    'Technology': [
        'cloud storage', 'smart home devices', 'wireless earbuds', 'laptops',
        'smartphones', 'tablets', 'monitors', 'mechanical keyboards',
        'VPN services', 'password managers', 'backup solutions', 'mesh WiFi',
        'streaming devices', 'e-readers', 'smartwatches', 'tech support'
    ],
    'Programming & Development': [
        'async/await', 'REST APIs', 'database indexing', 'authentication',
        'caching strategies', 'error handling', 'code reviews', 'CI/CD',
        'Docker containers', 'microservices', 'GraphQL', 'TypeScript',
        'React hooks', 'Python decorators', 'Git workflows', 'testing'
    ],
    'Gaming': [
        'Elden Ring', 'Baldur\'s Gate 3', 'indie games', 'roguelikes',
        'puzzle games', 'RPG mechanics', 'multiplayer games', 'game mods',
        'speedrunning', 'achievement hunting', 'game design', 'boss fights',
        'open world games', 'narrative games', 'retro games', 'gaming setups'
    ],
    'Science & Education': [
        'quantum mechanics', 'climate science', 'neuroscience', 'astronomy',
        'biology basics', 'chemistry concepts', 'mathematics', 'physics',
        'online courses', 'study techniques', 'research methods', 'STEM careers',
        'scientific method', 'critical thinking', 'data analysis', 'experiments'
    ],
    'Entertainment & Media': [
        'Dune Part Two', 'new series recommendations', 'classic films',
        'documentaries', 'podcasts', 'audiobooks', 'music albums',
        'concert experiences', 'book series', 'streaming services',
        'anime recommendations', 'TV show finales', 'movie theories',
        'director styles', 'genre discussions', 'media criticism'
    ],
    'Sports & Fitness': [
        'marathon training', 'weightlifting', 'yoga practice', 'cycling',
        'swimming', 'running form', 'home workouts', 'gym etiquette',
        'sports nutrition', 'recovery methods', 'CrossFit', 'climbing',
        'team sports', 'athletic performance', 'fitness goals', 'sports analysis'
    ],
    'Travel & Lifestyle': [
        'Japan', 'Iceland', 'New Zealand', 'Portugal', 'Thailand',
        'Italy', 'Norway', 'Costa Rica', 'Greece', 'Vietnam',
        'minimalism', 'sustainable living', 'urban vs rural', 'remote work',
        'digital nomad life', 'cultural experiences', 'local cuisine'
    ],
    'News & Current Events': [
        'technology regulation', 'climate policy', 'economic trends',
        'social movements', 'international relations', 'election analysis',
        'public health', 'education reform', 'urban development',
        'environmental initiatives', 'policy changes', 'civic engagement',
        'media literacy', 'community issues', 'global cooperation'
    ],
    'Off-Topic': [
        'weird dreams', 'childhood memories', 'unpopular opinions',
        'strange coincidences', 'life observations', 'random questions',
        'funny stories', 'irrational fears', 'guilty pleasures',
        'pet photos', 'cooking disasters', 'DIY projects',
        'collection hobbies', 'language quirks', 'time perception'
    ]
}

# Reply templates
REPLY_TEMPLATES = [
    "Thanks for sharing this! I've had similar experiences and found that {} really helps. Have you tried that approach?",

    "Interesting perspective. I see where you're coming from, though I think {} might also be a factor to consider.",

    "I struggled with this too. What worked for me was {}. Not sure if it'll work for your situation, but worth a try!",

    "Great question! From my experience, {} tends to be the most reliable option. Others might have different opinions though.",

    "I'm actually dealing with something similar right now. Did you find a solution? I'd love to hear what ended up working for you.",

    "This is really helpful, thanks! Quick follow-up question: {}?",

    "I disagree slightly - I think {} is more important in this context. But I see your point about the other factors.",

    "Totally agree with this. I'd also add that {} is worth considering, especially if you're looking for {}.",

    "Can you elaborate on {}? I'm curious about the details because I'm considering something similar.",

    "I tried this last year and had mixed results. {} worked well, but I ran into issues with {}. Your mileage may vary.",

    "This is exactly the kind of discussion we need! I've been thinking about {} a lot lately and your points really resonate.",

    "Have you looked into {}? I found it made a big difference when I was in a similar situation.",

    "Not to be that person, but I think {} might be better suited for this. Just my two cents!",

    "Wow, I never thought about it that way. {} is definitely something I'll need to reconsider now.",

    "Following this thread because I'm interested in the same thing. Hope you get some good answers!",
]

def generate_realistic_name(used_names):
    """Generate a unique realistic name"""
    max_attempts = 100
    for _ in range(max_attempts):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        full_name = f"{first} {last}"
        if full_name not in used_names:
            used_names.add(full_name)
            return first, last
    # Fallback: add middle initial
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    middle_initial = chr(random.randint(65, 90))
    return first, f"{middle_initial}. {last}"

def generate_username(first, last):
    """Generate username from name"""
    # Various username formats
    formats = [
        f"{first.lower()}.{last.lower()}",
        f"{first.lower()}{last.lower()}",
        f"{first.lower()}_{last.lower()}",
        f"{first[0].lower()}{last.lower()}",
    ]
    return random.choice(formats)

def generate_post_title(category_name):
    """Generate category-appropriate post title"""
    if category_name not in POST_TITLE_TEMPLATES:
        category_name = 'General Discussion'

    template = random.choice(POST_TITLE_TEMPLATES[category_name])
    topics = TOPIC_WORDS.get(category_name, TOPIC_WORDS['General Discussion'])

    # Count placeholders in template
    placeholder_count = template.count('{}')

    if placeholder_count == 0:
        return template
    elif placeholder_count == 1:
        return template.format(random.choice(topics))
    else:
        # For templates with multiple placeholders
        selected_topics = random.sample(topics, min(placeholder_count, len(topics)))
        return template.format(*selected_topics)

def generate_post_content(title, category_name):
    """Generate realistic post content matching title and category"""
    generators = {
        'General Discussion': generate_general_post,
        'Technology': generate_tech_post,
        'Programming & Development': generate_programming_post,
        'Gaming': generate_gaming_post,
        'Science & Education': generate_science_post,
        'Entertainment & Media': generate_entertainment_post,
        'Sports & Fitness': generate_sports_post,
        'Travel & Lifestyle': generate_travel_post,
        'News & Current Events': generate_news_post,
        'Off-Topic': generate_offtopic_post,
    }

    generator = generators.get(category_name, generate_general_post)
    return generator(title)

def generate_reply_content():
    """Generate contextual reply content"""
    template = random.choice(REPLY_TEMPLATES)

    # Fill in placeholders with contextual phrases
    contextual_phrases = [
        "taking a step back and reassessing",
        "breaking it down into smaller parts",
        "getting input from others",
        "trying a different approach",
        "focusing on the fundamentals",
        "being patient and persistent",
        "doing more research",
        "starting with the basics",
        "learning from mistakes",
        "staying consistent",
    ]

    placeholder_count = template.count('{}')
    if placeholder_count > 0:
        phrases = random.sample(contextual_phrases, min(placeholder_count, len(contextual_phrases)))
        try:
            return template.format(*phrases)
        except:
            return template.replace('{}', random.choice(contextual_phrases))

    return template

def update_users(app):
    """Update all user names and emails (except admin and testuser)"""
    with app.app_context():
        users = User.query.filter(User.id > 2).all()  # Skip admin and testuser
        used_names = set()

        print(f"\nUpdating {len(users)} users...")

        for i, user in enumerate(users, 1):
            first, last = generate_realistic_name(used_names)
            username = generate_username(first, last)
            email = f"{username}@example.com"

            user.username = username
            user.email = email

            if i % 20 == 0:
                db.session.commit()
                print(f"  Updated {i}/{len(users)} users...")

        db.session.commit()
        print(f"✓ Updated {len(users)} users successfully!")

        # Show samples
        print("\nSample updated users:")
        samples = User.query.filter(User.id.between(3, 7)).all()
        for user in samples:
            print(f"  {user.id}: {user.username} ({user.email})")

def update_posts(app):
    """Update all post titles and content"""
    with app.app_context():
        posts = Post.query.all()

        print(f"\nUpdating {len(posts)} posts...")

        for i, post in enumerate(posts, 1):
            category_name = post.category.name
            title = generate_post_title(category_name)
            content = generate_post_content(title, category_name)

            post.title = title
            post.content = content

            if i % 100 == 0:
                db.session.commit()
                print(f"  Updated {i}/{len(posts)} posts...")

        db.session.commit()
        print(f"✓ Updated {len(posts)} posts successfully!")

        # Show samples
        print("\nSample updated posts:")
        samples = Post.query.limit(3).all()
        for post in samples:
            print(f"  [{post.category.name}] {post.title}")
            print(f"    {post.content[:80]}...")

def update_replies(app):
    """Update all reply content"""
    with app.app_context():
        replies = Reply.query.all()

        print(f"\nUpdating {len(replies)} replies...")

        for i, reply in enumerate(replies, 1):
            reply.content = generate_reply_content()

            if i % 100 == 0:
                db.session.commit()
                print(f"  Updated {i}/{len(replies)} replies...")

        db.session.commit()
        print(f"✓ Updated {len(replies)} replies successfully!")

        # Show samples
        print("\nSample updated replies:")
        samples = Reply.query.limit(3).all()
        for reply in samples:
            print(f"  {reply.content[:80]}...")

def verify_data(app):
    """Verify the updated data"""
    with app.app_context():
        print("\n" + "="*60)
        print("VERIFICATION RESULTS")
        print("="*60)

        # Counts
        user_count = User.query.count()
        post_count = Post.query.count()
        reply_count = Reply.query.count()

        print(f"\nRecord counts:")
        print(f"  Users: {user_count} (expected: 102)")
        print(f"  Posts: {post_count} (expected: 1001)")
        print(f"  Replies: {reply_count} (expected: 3004)")

        # Check for generic patterns
        generic_users = User.query.filter(User.username.like('user%')).count()
        print(f"\nGeneric usernames remaining: {generic_users}")

        # Sample data
        print("\nSample realistic data:")
        print("\nUsers:")
        for user in User.query.filter(User.id.between(3, 7)).all():
            print(f"  • {user.username}")

        print("\nPosts:")
        for post in Post.query.limit(5).all():
            print(f"  • [{post.category.name}] {post.title}")

        print("\nReplies:")
        for reply in Reply.query.limit(3).all():
            print(f"  • {reply.content[:70]}...")

        print("\n" + "="*60)

def main():
    """Main update function"""
    print("="*60)
    print("BBS FORUM DATA UPDATE SCRIPT")
    print("="*60)
    print("\nThis will update:")
    print("  • 100 user names and emails (keeping admin and testuser)")
    print("  • 1,001 post titles and content")
    print("  • 3,004 reply content")
    print("\nDatabase backup should exist at: bbs_forum.db.backup")

    response = input("\nProceed with update? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Update cancelled.")
        return

    app = create_app()

    try:
        # Update in order
        update_users(app)
        update_posts(app)
        update_replies(app)

        # Verify results
        verify_data(app)

        print("\n✓ All updates completed successfully!")
        print("\nYou can now start the server with: python run.py")
        print("Visit http://localhost:5001 to see the realistic data")

    except Exception as e:
        print(f"\n✗ Error during update: {e}")
        print("\nTo restore from backup:")
        print("  mv bbs_forum.db.backup bbs_forum.db")
        raise

if __name__ == '__main__':
    main()
