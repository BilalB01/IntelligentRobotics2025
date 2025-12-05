from setuptools import setup

package_name = 'my_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jouw Naam',
    maintainer_email='ubuntu@todo.todo',
    description='batterijspanning van de batterij',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'battery_publisher = my_robot.battery_publisher:main',
            'battery_monitor = my_robot.battery_monitor:main',
        ],
    },
)
