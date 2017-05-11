import math
import numpy as np

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates Rotation Matrix given euler angles.
def eulerAnglesToRotationMatrix(theta) :
     
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                                 
    R = np.dot(R_z, np.dot( R_y, R_x ));
 
    return R;

class RobotPose:
	''' Robot pose class relative to world

	'''
	def __init__(self, R = np.matrix([[1, 0, 0],[0, 1, 0], [0, 0, 1]]), 
		T = np.matrix([[0], [0], [0]])):
		self.R = R;
		self.T = T;
		self.tf = constructTfMat(self.R, self.T);

	#getter rotation matrix
	def getRotationMat(self):
		return self.tf[np.ix_([0, 1, 2],[0, 1, 2])];

	#setter rotation matrix
	def setRotationMat(self, rotMat):
		self.R = rotMat;
		self.tf = constructTfMat(self.R, self.T);

	#getter translation matrix
	def getTranslationMat(self):
		return self.tf[np.ix_([0, 1, 2],[3])];

	#setter translation matrix
	def setTranslationMat(self, transMat):
		self.T = transMat;
		self.tf = constructTfMat(self.R, self.T);

	# Calculates rotation matrix to euler angles
	def getEulerAngles(self):
	    assert(isRotationMatrix(self.R))
	     
	    sy = math.sqrt(self.R[0,0] * self.R[0,0] +  self.R[1,0] * self.R[1,0])
	     
	    singular = sy < 1e-6
	 
	    if  not singular :
	        x = math.atan2(self.R[2,1] , self.R[2,2])
	        y = math.atan2(-self.R[2,0], sy)
	        z = math.atan2(self.R[1,0], self.R[0,0])
	    else :
	        x = math.atan2(-self.R[1,2], self.R[1,1])
	        y = math.atan2(-self.R[2,0], sy)
	        z = 0
	 
	    return np.array([x, y, z]);

# constructs 4x4 transformation matrix from rotation and translation matrices
def constructTfMat(R, T):
	s = np.matrix([0, 0, 0, 1]);
	tr = np.concatenate((R, T), axis=1);
	tf = np.concatenate((tr, s), axis=0);
	return tf;

# test program
def main():
	rp = RobotPose();
	print "Pose: X"
	print rp.R;
	print "Pose: T"
	print rp.T;
	print rp.getRotationMat();

if __name__ == '__main__':
	main();