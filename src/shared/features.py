class LesionFeatures:
  def __init__(self, asymmetryScore):
    self.asymmetry = asymmetryScore
    self.featureNamesList = ['Asymmetry']

  def featuresList(self):
    return [self.asymmetry]
