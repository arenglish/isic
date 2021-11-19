class LesionFeatures:
  def __init__(self, asymmetry, color):
    self.asymmetry = asymmetry
    self.color = color
    self.featureNamesList = ['Color', 'Asymmetry']

  def featuresList(self):
    return [self.color, self.asymmetry]
