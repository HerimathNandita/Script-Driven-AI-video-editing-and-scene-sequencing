import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def parse_script(text):
    """
    Parses a script text and returns a list of scenes.
    Each scene is a dictionary with 'header' and 'content'.
    """
    scenes = []
    current_scene = None
    
    # Robust Regex: Matches "Scene 1", "INT.", "1.", "1)", etc.
    # Allow simple numbering like "1. The park"
    scene_header_regex = re.compile(r'^\s*(INT\.|EXT\.|Scene\s+\d+|^\d+\.|^\d+\))', re.IGNORECASE)
    
    lines = text.split('\n')
    
    found_any_header = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if scene_header_regex.match(line):
            found_any_header = True
            if current_scene:
                scenes.append(current_scene)
            current_scene = {
                'header': line,
                'content': []
            }
        else:
            if current_scene:
                current_scene['content'].append(line)
            else:
                # If content appears before any header, create a default first scene
                if not found_any_header:
                     current_scene = {
                        'header': 'Scene 1 (Auto-Detected)',
                        'content': [line]
                     }
                     found_any_header = True
                
    if current_scene:
        scenes.append(current_scene)
        
    # fallback: if still empty but text exists
    if not scenes and text.strip():
        scenes.append({
            'header': 'Scene 1 (Default)',
            'content': [text.strip()]
        })

    # Calculate estimated duration for each scene
    for scene in scenes:
        # Heuristic: 5 seconds base + 0.5 seconds per word in content
        word_count = 0
        for line in scene['content']:
            word_count += len(line.split())
        
        duration = 5.0 + (word_count * 0.5)
        scene['estimated_duration'] = duration
        
    return scenes


def calculate_text_similarity(text1, text2):
    """
    Calculates semantic similarity between two texts using TF-IDF and Cosine Similarity.
    Used for matching script dialogue with video audio.
    """
    if not text1 or not text2:
        return 0.0
        
    try:
        # Create a tiny corpus of just these two texts
        corpus = [text1, text2]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return float(similarity[0][0])
    except Exception as e:
        # Fallback to simple set intersection if sklearn fails or empty vocab
        return 0.0
