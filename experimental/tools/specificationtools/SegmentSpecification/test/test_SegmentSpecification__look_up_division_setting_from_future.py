from experimental import *


def test_SegmentSpecification__look_up_division_setting_from_future_01():
    '''From-future division setting lookup.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_division_command = blue_segment.timespan.start_offset.look_up_division_setting('Voice 1')
    red_segment.set_divisions(blue_division_command)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(4, 8), (4, 8)])
    blue_segment.set_divisions([(3, 16), (5, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_setting_from_future_02():
    '''From-future division setting lookup with reverse callback.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_division_command = blue_segment.timespan.start_offset.look_up_division_setting('Voice 1')
    blue_division_command = blue_division_command.reflect()
    red_segment.set_divisions(blue_division_command)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(4, 8), (4, 8)])
    blue_segment.set_divisions([(3, 16), (5, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_setting_from_future_03():
    '''From-future division setting lookup with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_division_command = blue_segment.timespan.start_offset.look_up_division_setting('Voice 1')
    blue_division_command = blue_division_command.reflect()
    red_segment.set_divisions(blue_division_command)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(4, 8), (4, 8)])
    blue_segment.set_divisions([(3, 16), (5, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_division_setting_from_future_04():
    '''From-future division setting lookup with reverse callbacks.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    red_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_division_command = blue_segment.timespan.start_offset.look_up_division_setting('Voice 1')
    blue_division_command = blue_division_command.reflect()
    blue_division_command = blue_division_command.reflect()
    red_segment.set_divisions(blue_division_command)
    red_segment.set_rhythm(library.sixteenths)
    blue_segment.set_time_signatures([(4, 8), (4, 8)])
    blue_segment.set_divisions([(3, 16), (5, 16)])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
