import random

class Slide:
    def __init__(self):
       self.pictures = []

    def add_picture(self, picture):
        self.pictures.append(picture)

    def get_tags(self):
        tags = []
        for picture in self.pictures:
            for tag in picture.tags:
                if tag not in tags:
                    tags.append(tag)
        return tags

    def __str__(self):
        return " ".join([str(x) for x in self.pictures])

class Picture:
    def __init__(self, pid, vertical, tags):
        self.id = pid
        self.vertical = vertical
        self.tags = tags

    def __str__(self):
        return str(self.id)

def load_pictures(path):
    file = open(path, "r")
    content = file.read()
    file.close()

    output = []

    for i, line in enumerate(content.split("\n")[1:]):
        if line == "":
            continue
        data = line.split(" ")
        vertical = data[0] == "V"
        tags = data[2:]
        output.append(Picture(i, vertical, tags))

    return output

def generate_slideshow_random(pictures):
    
    #random.shuffle(pictures)

    slide = None

    slideshow = []
    incomplete = []
    
    for picture in pictures:
        if picture.vertical:
            if incomplete:
                slide = incomplete[-1]
                for incomplete_slide in incomplete:
                    if tags_in_common(picture.tags, incomplete_slide.pictures[0].tags):
                        slide = incomplete_slide
                slide.add_picture(picture)
                slideshow.append(slide)
                incomplete.remove(slide)
            else:
                slide = Slide()
                slide.add_picture(picture)
                incomplete.append(slide)
                
        else:
            slide = Slide()
            slideshow.append(slide)
            slide.add_picture(picture)
    
    return slideshow

def generate_slideshow_sort(pictures):
    slides = generate_slideshow_random(pictures)
    return sorted(slides, key=lambda x: x.pictures[0].tags[0])

def get_tag_scores(pictures):
    scores = {}
    for picture in pictures:
        for tag in picture.tags:
            if tag not in scores:
                scores[tag] = 0
            scores[tag] += 1
    return scores

def generate_slideshow_popular(pictures):
    scores = get_tag_scores(pictures)

    slides = generate_slideshow_random(pictures)
    for slide in slides:
        score = 0
        for tag in slide.get_tags():
            score += scores[tag]
        slide.score = score
    return sorted(slides, key=lambda x: x.score)

def tags_in_common(tags1, tags2):
    count = 0
    for tag1 in tags1:
        for tag2 in tags2:
            if tag1 == tag2:
                count += 1
    return count

def generate_slideshow_relation(picture):
    slides = generate_slideshow_random(pictures)
    out = [slides.pop()]
    tags = out[0].get_tags()
    while slides:
        for i, slide in enumerate(slides):
            now_tags = slide.get_tags()
            if tags_in_common(tags, now_tags) > 0:
                out.append(slides.pop(i))
                tags = now_tags
                break
        else:
            out.append(slides.pop())
            tags = out[-1].get_tags()
        #if len(slides) % 50 == 0:
        #    print(len(slides))
    return out

def get_most_popular_tag(tags, scores):
    most_popular = None
    most_popular_score = 0
    for tag in tags:
        if scores[tag] > most_popular_score:
            most_popular_score = scores[tag]
            most_popular = tag
    return most_popular

def generate_slideshow(pictures):
    scores = get_tag_scores(pictures)
    slides = generate_slideshow_random(pictures)
    #for slide in slides:
    #    slide.scores = scores
    return sorted(slides, key=lambda x: get_most_popular_tag(x.get_tags(), scores) + "".join(x.get_tags()))

def save(slides, path):
    file = open(path, "w")
    file.write(str(len(slides)) + "\n" + "\n".join([str(slide) for slide in slides]))
    file.close()
    #print(str(len(slides)) + "\n" + "\n".join([str(slide) for slide in slides]))


names = [
    "a_example",
    "c_memorable_moments",
    "e_shiny_selfies",
    "d_pet_pictures",
    "b_lovely_landscapes",
]

for name in names:
    print(name + "...")
    pictures = load_pictures(name + ".txt")
    slides = generate_slideshow(pictures)
    save(slides, name + ".out")
