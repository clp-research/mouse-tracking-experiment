# TO DO: Pause after first DP

# SSML template for text to speech synthesis
# Text: "Please click on the ", "Next: The "

ssml_template =  """
    <?xml version="1.0"?>
    <speak version="1.1" xmlns="http://www.w3.org/2001/10/synthesis"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.w3.org/2001/10/synthesis
                     http://www.w3.org/TR/speech-synthesis11/synthesis.xsd"
           xml:lang="en-GB">
                    <s>
                        {intro}<prosody rate="{prosody_rate}">{article}{text}{punctuation}</prosody>
                    </s>
            </prosody>
    </speak>
    """

def ssml_utterance(string, string_tagged=False, prosody_rate = "medium", intro = "Next: ",article="The ", punctuation=".", ssml_template=ssml_template):

    ssml_template = ssml_template.format(article=article, punctuation=punctuation, intro=intro, prosody_rate="{prosody_rate}",text="{text}")

    # adjust prosody rate (x-slow, slow, medium, fast, x-fast, n%)
    ssml_template = ssml_template.format(prosody_rate=prosody_rate, text="{text}")

    # add string to SSML template and return utterance
    utterance = ssml_template.format(text=str(string))
    print ("string: '{text}', prosody rate: '{prosody_rate}'".format(text=string, prosody_rate=prosody_rate))
    return utterance
