#!/usr/bin/python


import rospy
import actionlib
import actionlib_tutorials.msg

from control_msgs.msg import FollowJointTrajectoryAction,FollowJointTrajectoryActionGoal, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class youbot_action_server(object):

    def __init__(self):
        
        #create action server which can deal with 8-DOF "follow_joint_trajectory" action
        self._as = actionlib.SimpleActionServer("moveit/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction, execute_cb=self.execute_cb, auto_start = False)
        
        
        #create two publishers, one for publishing the topic to base and another to arm
        self.pub1 = rospy.Publisher("base_controller/follow_joint_trajectory/goal", FollowJointTrajectoryActionGoal, queue_size=1)
        
        self.arm_client = actionlib.SimpleActionClient('arm_1/arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        
#        self.pub2 = rospy.Publisher("arm1/arm_controller/follow_joint_trajectory/goal", FollowJointTrajectoryActionGoal, queue_size=1)
        
        self._as.start()
   
    def execute_cb(self, goal):
        
        arm_action = FollowJointTrajectoryAction()
        
        #create two seperate goals 
        base_fjtag = FollowJointTrajectoryActionGoal()
        arm_fjtag = FollowJointTrajectoryActionGoal()
        
                
#        base_fjtag.goal_id = goal.goal_id
#        base_fjtag.header.stamp = goal.goal_id.stamp
        
        base_goal = FollowJointTrajectoryGoal()
        base_jt = JointTrajectory()
        base_jt.joint_names = ["virtual_x", "virtual_y", "virtual_theta"] 
        
#        arm_fjtag.goal_id = goal.goal_id
#        arm_fjtag.header.stamp = goal.goal_id.stamp
        
        arm_goal = FollowJointTrajectoryGoal()
        arm_jt = JointTrajectory()
        arm_jt.joint_names = ["arm_joint_1", "arm_joint_2", "arm_joint_3","arm_joint_4","arm_joint_5"] 
        
        for pt in goal.trajectory.points:
            
            pt_temp = JointTrajectoryPoint()
            
            #allocate the first three pt.position(for base) elements to base trajectory
#            pt_temp.positions = pt.positions[5:8]
#            pt_temp.velocities = pt.velocities[5:8]
#            pt_temp.accelerations = pt.accelerations[5:8]
            pt_temp.positions.append(pt.positions[6])
            pt_temp.positions.append(pt.positions[7])
            pt_temp.positions.append(pt.positions[5])
            
            pt_temp.time_from_start = pt.time_from_start
            base_jt.points.append(pt_temp)
            
            pt_temp = JointTrajectoryPoint()
            
            #allocate the last five pt.position(for arm) elements to arm trajectory
            
            pt_temp.positions = pt.positions[0:5]
#            pt_temp.velocities = pt.velocities[0:5]
#            pt_temp.accelerations = pt.accelerations[0:5]
#            
            pt_temp.time_from_start = pt.time_from_start
            
            arm_jt.points.append(pt_temp)
            
        base_goal.trajectory = base_jt
        arm_goal.trajectory = arm_jt
            
        base_fjtag.goal = base_goal
        arm_fjtag.goal = arm_goal
        
        arm_action = arm_goal
        
        # check that preempt has not been requested by the client
        if self._as.is_preempt_requested():
           sys.exit() 
            #if preempted, can do something here
            
           
        else:
            self.pub1.publish(base_fjtag)
            self.arm_client.send_goal_and_wait(arm_action)
#           self.pub2.publish(arm_fjtag)
             

     
if __name__ == '__main__':
    rospy.init_node('youbot_action_server')
    server = youbot_action_server() 
    rospy.spin()
