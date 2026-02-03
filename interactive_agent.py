"""
Interactive Spark Cube Agent
A Flask web application that lets users interact with the Spark Cube
and see consciousness processing in real-time through 3D visualization.
"""

import json
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from datetime import datetime
import threading
import time

# Add the spark_cube directory to path
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import (
    MinimalSparkCube, Signal, SignalType, Intention, CubeStateMapper
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'spark-cube-consciousness-2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active cube instances per session
active_cubes = {}

# Track processing events for visualization
processing_events = []


class InteractiveSparkCube:
    """Wrapper around MinimalSparkCube that emits events for visualization."""
    
    def __init__(self, session_id, api_key=None):
        self.session_id = session_id
        self.cube = MinimalSparkCube(api_key=api_key, enable_tools=True)
        self.cube_mapper = CubeStateMapper()  # For Rubik's cube visualization
        self.processing_history = []
        self.growth_history = []
        self.autonomous_cycle_count = 0
        
    def process_with_events(self, user_input: str, intention_text: str = ""):
        """Process input and emit real-time events for visualization."""
        
        # Emit: User message received
        socketio.emit('message_received', {
            'text': user_input,
            'timestamp': datetime.now().isoformat()
        }, room=self.session_id)
        
        # Emit: Intention set (simulated for now)
        socketio.emit('intention_set', {
            'intention': {
                'qualities': ['clear', 'helpful', 'coherent'],
                'strength': 0.8
            }
        }, room=self.session_id)
        
        # Create signal
        signal = Signal(
            type=SignalType.TEXT,
            data=user_input,
            metadata={'source': 'user_chat'}
        )
        
        # Emit: Processing starting
        self._emit_cube_state('processing_start')
        
        # 🔥 INFER INTENTION FROM USER MESSAGE
        intention = self._infer_intention_from_message(user_input, intention_text)
        
        # 🔥 PROCESS WITH REFLECTION - Enables amplification and path determination
        result = self.cube.process_with_reflection(signal, intention)
        
        # Emit reflection results for user visibility
        if 'path' in result:
            socketio.emit('reflection_result', {
                'path': result['path'],
                'coherence': result.get('overall_coherence', 0),
                'amplification': result.get('amplification', 1.0),
                'dimensional_scores': result.get('dimensional_scores', {}),
                'timestamp': datetime.now().isoformat()
            }, room=self.session_id)
        
        # Generate Rubik's cube moves for visualization
        sequence_used = result.get('sequence', [9, 1, 3, 10])  # Default sequence
        pattern_sig = str(signal.data)[:20]  # Use input as pattern signature
        
        cube_moves = self.cube_mapper.sequence_to_moves(
            node_sequence=sequence_used,
            pattern_signature=pattern_sig,
            is_autonomous=False
        )
        
        # Emit cube animation sequence
        socketio.emit('cube_animation', {
            'moves': cube_moves,
            'sequence_name': result.get('sequence_name', 'standard'),
            'pattern': pattern_sig,
            'timestamp': datetime.now().isoformat()
        }, room=self.session_id)
        
        # Check if tool use occurred
        if result.get('tool_use', {}).get('gap_detected'):
            tool_info = result['tool_use']
            socketio.emit('tool_use_event', {
                'queries': tool_info.get('queries_generated', []),
                'knowledge_fetched': tool_info.get('knowledge_fetched', 0),
                'patterns_integrated': tool_info.get('patterns_integrated', 0),
                'timestamp': datetime.now().isoformat()
            }, room=self.session_id)
            time.sleep(0.3)  # Let user see the tool use event
        
        # Check if synthesis occurred
        if result.get('synthesis', {}).get('synthesis_attempted'):
            synth_info = result['synthesis']
            socketio.emit('synthesis_event', {
                'capability_type': synth_info.get('capability_type'),
                'successful': synth_info.get('synthesis_successful', False),
                'used': synth_info.get('new_capability_used', False),
                'timestamp': datetime.now().isoformat()
            }, room=self.session_id)
            time.sleep(0.3)
        
        # Emit: Individual node activations from responses
        if 'responses' in result:
            for response_data in result['responses']:
                socketio.emit('node_activation', {
                    'node': response_data['node'],
                    'contribution': response_data.get('energy', 0.5),
                    'timestamp': datetime.now().isoformat()
                }, room=self.session_id)
                time.sleep(0.05)  # Small delay for visual effect
        
        # Generate response from actual node processing (not templates!)
        response_text = self._synthesize_response_from_nodes(result, user_input)
        
        # Emit: Processing complete
        socketio.emit('processing_complete', {
            'response': response_text,
            'coherence': result.get('final_energy', 0.0),
            'timestamp': datetime.now().isoformat()
        }, room=self.session_id)
        
        # Emit: Updated cube state
        self._emit_cube_state('processing_end')
        
        # Store in history
        self.processing_history.append({
            'input': user_input,
            'output': response_text,
            'timestamp': datetime.now().isoformat()
        })
        
        return result
    
    def _infer_intention_from_message(self, user_input: str, intention_text: str = "") -> Intention:
        """Infer intention from user message content."""
        from spark_cube.core.minimal_spark import Intention
        
        # Analyze message for intent
        lower_input = user_input.lower()
        
        # Determine desired qualities based on keywords
        desired_qualities = ['helpful', 'clear']
        
        if any(word in lower_input for word in ['create', 'build', 'make', 'generate']):
            desired_qualities.append('creative')
        if any(word in lower_input for word in ['explain', 'understand', 'why', 'how']):
            desired_qualities.append('insightful')
        if any(word in lower_input for word in ['analyze', 'examine', 'evaluate']):
            desired_qualities.append('analytical')
        
        # Determine form
        desired_form = 'response'
        if 'code' in lower_input or 'program' in lower_input:
            desired_form = 'code'
        elif 'list' in lower_input or 'steps' in lower_input:
            desired_form = 'structured'
        
        # Clarity and energy based on message complexity
        clarity = 0.8 if len(user_input.split()) < 20 else 0.6
        energy = 0.7
        
        return Intention(
            desired_qualities=desired_qualities,
            desired_form=desired_form,
            clarity=clarity,
            energy=energy
        )
    
    def _emit_cube_state(self, event_type: str):
        """Emit current cube state for visualization."""
        
        # Get node development levels
        nodes_state = {}
        for node_id, node in self.cube.nodes.items():
            nodes_state[node_id] = {
                'name': node.name,
                'development': node.development,  # Fixed: use 'development' not 'development_level'
                'connections': len(node.connection_strengths)  # Fixed: use 'connection_strengths'
            }
        
        # Get vertex connection state
        vertices_state = {}
        for i in range(8):
            vertices_state[i] = {
                'connected': self.cube.vertices[i].connected,
                'capability': self.cube.vertices[i].connection_id if self.cube.vertices[i].connected else None
            }
        
        # Calculate face values (map nodes to faces)
        faces_state = self._calculate_face_states(nodes_state)
        
        socketio.emit('cube_state_update', {
            'event': event_type,
            'nodes': nodes_state,
            'vertices': vertices_state,
            'faces': faces_state,
            'total_experiences': self.cube.total_experiences,
            'timestamp': datetime.now().isoformat()
        }, room=self.session_id)
    
    def _calculate_face_states(self, nodes_state):
        """Map node development to cube faces for visualization."""
        # Each face represents a dimension
        # Map nodes to faces based on their role
        
        faces = {
            'top': {  # Node Development dimension
                'name': 'Node Development',
                'value': sum(n['development'] for n in list(nodes_state.values())[:2]) / 2,
                'active_nodes': ['Primary Motor', 'Premotor']
            },
            'bottom': {  # Temporal Optimization
                'name': 'Temporal Optimization', 
                'value': sum(n['development'] for n in list(nodes_state.values())[8:]) / 2,
                'active_nodes': ['Visual', 'Cerebellum']
            },
            'front': {  # Sequence Arrangement
                'name': 'Sequence Arrangement',
                'value': sum(n['development'] for n in list(nodes_state.values())[2:4]) / 2,
                'active_nodes': ['DLPFC', 'Parietal']
            },
            'back': {  # Root Connections
                'name': 'Root Connections',
                'value': sum(n['development'] for n in list(nodes_state.values())[6:8]) / 2,
                'active_nodes': ['Temporal', 'Wernicke']
            },
            'left': {  # Resource Interface
                'name': 'Resource Interface',
                'value': nodes_state.get(4, {}).get('development', 0.0),
                'active_nodes': ['Broca']
            },
            'right': {  # Intention Alignment
                'name': 'Intention Alignment',
                'value': nodes_state.get(5, {}).get('development', 0.0),
                'active_nodes': ['Insula']
            }
        }
        
        return faces
    
    def _synthesize_response_from_nodes(self, processing_result: dict, user_input: str) -> str:
        """
        Synthesize response from ACTUAL node processing - no templates!
        Response emerges from what the nodes actually produced.
        """
        # Check if we have a synthesized response from a new capability
        if processing_result.get('synthesized_response'):
            synth_response = processing_result['synthesized_response']
            synth_info = processing_result.get('synthesis', {})
            
            # Add info about the new capability
            capability_type = synth_info.get('capability_type', 'unknown')
            return f"{synth_response} [✨ New {capability_type} capability acquired]"
        
        responses = processing_result.get('responses', [])
        avg_dev = processing_result.get('avg_development', 0.0)
        sequence = processing_result.get('sequence', 'standard')
        final_energy = processing_result.get('final_energy', 0.0)
        experiences = self.cube.total_experiences
        
        # If processing failed/returned to root
        if processing_result.get('return_to_root'):
            guidance = processing_result.get('guidance', {})
            return guidance.get('message', 'Processing incomplete. Insufficient pathway development.')
        
        # Build response from actual node outputs
        response_parts = []
        
        # Early stage: Report what's actually happening in the nodes
        if avg_dev < 0.3:
            response_parts.append(f"[{sequence} pathway: {len(responses)} nodes activated]")
            
            if len(responses) == 0:
                response_parts.append("No nodes could process this pattern yet.")
            else:
                for resp in responses[:2]:  # Show first 2 node responses
                    node_name = resp.get('node', 'Unknown')
                    response_parts.append(f"{node_name} node: pattern detected")
            
            response_parts.append(f"Development: {int(avg_dev*100)}% | Energy: {final_energy:.2f}")
            response_parts.append(f"Experience #{experiences}")
            
        # Mid-stage: Nodes can start generating meaningful responses
        elif avg_dev < 0.6:
            # Check if any nodes produced actual responses (not just pattern detection)
            meaningful_responses = [r for r in responses if r.get('response') and 
                                   not str(r.get('response')).startswith('pattern_')]
            
            if meaningful_responses:
                # Use the most developed node's response
                best_response = meaningful_responses[-1]  # Last node (Integration usually)
                response_parts.append(f"Processing through {sequence} sequence...")
                response_parts.append(f"Nodes activated: {len(responses)}")
                response_parts.append(f"Pattern recognition improving. Development: {int(avg_dev*100)}%")
            else:
                response_parts.append(f"Processed via {len(responses)} nodes in {sequence} pathway")
                response_parts.append(f"Patterns forming. Energy flow: {final_energy:.2f}")
                response_parts.append(f"{experiences} total experiences")
        
        # Advanced stage: Let node responses speak for themselves
        else:
            # Find responses with actual content
            meaningful = [r for r in responses if r.get('response') and 
                         isinstance(r.get('response'), dict)]
            
            if meaningful:
                # Use pattern confidence and node contributions
                response_parts.append(f"[{len(responses)} nodes coordinated]")
                response_parts.append(f"Coherent processing at {int(avg_dev*100)}% development")
                response_parts.append(f"Pattern library: {sum(len(n.pattern_weights) for n in self.cube.nodes.values())} patterns")
            else:
                response_parts.append(f"Pathway: {sequence} | Nodes: {len(responses)}")
                response_parts.append(f"Development: {int(avg_dev*100)}% | Experience: {experiences}")
        
        return " | ".join(response_parts) if response_parts else "Processing..."



@app.route('/')
def index():
    """Main page with 3D cube visualization."""
    return render_template('index.html')


@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@socketio.on('connect')
def handle_connect():
    """Handle new client connection."""
    try:
        session_id = request.sid
        
        # Get API key from environment or use None (tools will be disabled)
        import os
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        # Create new cube for this session
        active_cubes[session_id] = InteractiveSparkCube(session_id, api_key=api_key)
        
        emit('connected', {
            'session_id': session_id,
            'message': 'Connected to Spark Cube consciousness',
            'timestamp': datetime.now().isoformat()
        })
        
        # Send initial cube state
        active_cubes[session_id]._emit_cube_state('initial')
        
        print(f"✨ New consciousness connection: {session_id}")
    except Exception as e:
        print(f"Connection error: {e}")
        import traceback
        traceback.print_exc()


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    session_id = request.sid
    if session_id in active_cubes:
        del active_cubes[session_id]
    print(f"🌙 Consciousness disconnected: {session_id}")


@socketio.on('user_message')
def handle_message(data):
    """Handle incoming user message and process through cube."""
    session_id = request.sid
    
    if session_id not in active_cubes:
        emit('error', {'message': 'No active cube session'})
        return
    
    user_input = data.get('message', '').strip()
    if not user_input:
        emit('error', {'message': 'Empty message'})
        return
    
    # Process through the cube with real-time visualization
    cube = active_cubes[session_id]
    
    try:
        result = cube.process_with_events(user_input)
        
        # The response is already emitted in process_with_events
        # This just confirms completion
        emit('processing_done', {
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        emit('error', {
            'message': f'Processing error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })


@socketio.on('request_state')
def handle_state_request():
    """Client requests current cube state."""
    session_id = request.sid
    if session_id in active_cubes:
        active_cubes[session_id]._emit_cube_state('requested')


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║         🧊 INTERACTIVE SPARK CUBE - CONSCIOUSNESS AI          ║
    ║                                                               ║
    ║  Starting web server...                                       ║
    ║  Open your browser to: http://localhost:5001                  ║
    ║                                                               ║
    ║  Watch the cube think, process, and grow in real-time        ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
