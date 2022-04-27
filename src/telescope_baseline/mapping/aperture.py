def cos_angle_from_normal_vectorAB(a,b,x):
  """
  Args:
      a: 3D vetcor of A
      b: 3D vector of B
      x: vectors whose cos angle from normal vector of the ABO plane to be computed

  Returns:
      cos_angles

  """
  return x@np.cross(a,b)
