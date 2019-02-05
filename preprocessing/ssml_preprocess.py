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
                        {intro} <prosody rate="{prosody_rate}">The {text}.</prosody>
                    </s>
            </prosody>
    </speak>
    """

def modify_refexp(text, tagged):
    return text
    # get rid of double articles (i.e. initial 'the' resulting in 'the the ...')
    # ? check if there's an 'NN' in the refexp, if not: add one

#    result_text = ""
#    pause = '<break strength="x-weak"/>'
#    for word in text.split():
#        result_text += (word+" ")
#        if tagged[text.split().index(word)][1] == u'NN':
#            result_text += pause
#    return result_text

def ssml_utterance(refexp, refexp_tagged, prosody_rate = "medium", intro = "Next:", ssml_template=ssml_template):

    # adjust prosody rate for refexp (x-slow, slow, medium, fast, x-fast, n%)
    ssml_template = ssml_template.format(prosody_rate=prosody_rate, text="{text}", intro=intro)

    refexp = modify_refexp(refexp, refexp_tagged)

    # add refexp to SSML template and return utterance
    utterance = ssml_template.format(text=str(refexp))
    print ("refexp: '{text}', prosody rate: '{prosody_rate}'".format(text=refexp, prosody_rate=prosody_rate))
    return utterance
