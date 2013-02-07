from experimental.tools import *
import py


def test_ScoreSpecification__set_time_signatures_01():
    '''Works without segment specification.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    score_specification.set_divisions([(3, 16)])
    score_specification.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name, go=True)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_time_signatures_02():
    '''Works without division specification.
    '''
    py.test.skip('working on this one now')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    score_specification.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
