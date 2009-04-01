from abjad.core.interface import _Interface


class _Observer(_Interface):

   def __init__(self, _client, updateInterface):
      _Interface.__init__(self, _client)
      updateInterface._observers.append(self)

   ## PRIVATE METHODS ##

   def _makeSubjectUpdateIfNecessary(self):
      observerSubject = self._client._update
      if not observerSubject._currentToRoot:
         observerSubject._updateAll( )
