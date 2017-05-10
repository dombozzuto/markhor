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
	def __init__(self):
		self.R = np.matrix([[0, 0, 0],[0, 0, 0], [0, 0, 0]]);
		self.T = np.matrix([[0], [0], [0]]);

	#getter rotation matrix
	def getRotationMat(self):
		return self.R;

	#setter rotation matrix
	def setRotationMat(self, rotMat):
		self.R = rotMat;

	#getter translation matrix
	def getTranslationMat(self):
		return self.T;

	#setter translation matrix
	def setTranslationMat(self, transMat):
		self.T = transMat;

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

def main():
	rp = RobotPose();
	print "Pose: X"
	print rp.R;
	print "Pose: T"
	print rp.T;
	print rp.getEulerAngles();
	
if __name__ == '__main__':
	main();