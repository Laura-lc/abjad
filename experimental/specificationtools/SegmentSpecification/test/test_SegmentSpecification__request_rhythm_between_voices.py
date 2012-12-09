from abjad import *
from experimental import *


def test_SegmentSpecification__request_rhythm_between_voices_01():
    '''Rhythm material request between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.request_rhythm('Voice 2')
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_rhythm_between_voices_02():
    '''Rhythm material request between voices with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.request_rhythm('Voice 2', reverse=True)
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'])
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_rhythm_between_voices_03():
    '''Rhythm material request between voices with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.request_rhythm('Voice 2')
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'], reverse=True)
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_rhythm_between_voices_04():
    '''Rhythm material request between voices with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    voice_2_rhythm = red_segment.request_rhythm('Voice 2', reverse=True)
    red_segment.set_rhythm(voice_2_rhythm, contexts=['Voice 1'], reverse=True)
    red_segment.set_rhythm(library.dotted_sixteenths, contexts=['Voice 2'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__request_rhythm_between_voices_05():
    '''Rhythm material request between voices with multiple in-voice application.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures('Voice 1', 0, 1)
    second_measure = red_segment.select_background_measures('Voice 1', 1, 2)
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'], selector=first_measure)
    cell = red_segment.request_rhythm('Voice 1', anchor=first_measure)
    red_segment.set_rhythm(cell, contexts=['Voice 1'], selector=second_measure, rotation=Duration(-1, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 2'], selector=first_measure, rotation=Duration(-2, 32))
    red_segment.set_rhythm(cell, contexts=['Voice 2'], selector=second_measure, rotation=Duration(-3, 32))
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
