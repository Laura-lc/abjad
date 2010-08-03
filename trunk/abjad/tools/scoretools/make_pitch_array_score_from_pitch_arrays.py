from abjad.components.Score import Score
from abjad.components.Staff import Staff
from abjad.components.StaffGroup import StaffGroup


def make_pitch_array_score_from_pitch_arrays(pitch_arrays):
   r'''.. versionadded:: 1.1.2

   Change `pitch_arrays` to score with one staff per pitch array row. ::

      abjad> array_1 = pitchtools.PitchArray([
      ...   [1, (2, 1), ([-2, -1.5], 2)],
      ...   [(7, 2), (6, 1), 1]])
      abjad> array_2 = pitchtools.PitchArray([
      ...   [1, 1, 1],
      ...   [1, 1, 1]])

   ::

      abjad> score = scoretools.make_pitch_array_score_from_pitch_arrays(array_1, array_2)
      abjad> f(score)
      \new Score <<
              \new StaffGroup <<
                      \new Staff {
                              {
                                      \time 4/8
                                      r8
                                      d'8
                                      <bf bqf>4
                              }
                              {
                                      \time 3/8
                                      r8
                                      r8
                                      r8
                              }
                      }
                      \new Staff {
                              {
                                      \time 4/8
                                      g'4
                                      fs'8
                                      r8
                              }
                              {
                                      \time 3/8
                                      r8
                                      r8
                                      r8
                              }
                      }
              >>
      >>

   .. versionchanged:: 1.1.2
      renamed ``scoretools.pitch_arrays_to_score( )`` to
      ``scoretools.make_pitch_array_score_from_pitch_arrays( )``.
   '''

   from abjad.tools import measuretools

   score = Score([ ])
   staff_group = StaffGroup([ ])
   score.append(staff_group)
   number_staves = pitch_arrays[0].depth
   staves = Staff([ ]) * number_staves
   staff_group.extend(staves)

   for pitch_array in pitch_arrays:
      measures = measuretools.pitch_array_to_measures(pitch_array)
      for staff, measure in zip(staves, measures):
         staff.append(measure)
  
   return score 
