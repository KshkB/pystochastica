from core import JointDistribution

class RandVec(JointDistribution):

    def __init__(self, joint_pspace: dict) -> None:
        super().__init__(joint_pspace)
