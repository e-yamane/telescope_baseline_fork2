def test_cos_angle_from_normal_vectorAB():
  a=np.array([1,0,0])
  b=np.array([0,1,0])
  v=cos_angle_from_normal_vectorAB(a,b,[ np.cross(a,b)])
  assert v[0]==1
