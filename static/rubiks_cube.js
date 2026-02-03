/**
 * Rubik's Cube 3D Visualization
 * Displays AI processing as physical cube rotations
 */

class RubiksCube {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.cube = null;
        this.cubies = [];  // 27 individual mini-cubes
        this.animationQueue = [];
        this.isAnimating = false;
        this.autonomousMode = true;
        
        // Cubie size and spacing
        this.cubieSize = 0.95;
        this.cubeSpacing = 1.0;
        
        // Current cube state (tracking rotations)
        this.cubeState = this._initializeState();
        
        this.init();
    }
    
    init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a0a);
        
        // Camera
        this.camera = new THREE.PerspectiveCamera(
            45,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(8, 8, 8);
        this.camera.lookAt(0, 0, 0);
        
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 10);
        this.scene.add(directionalLight);
        
        const backLight = new THREE.DirectionalLight(0x6495ed, 0.3);
        backLight.position.set(-10, -10, -10);
        this.scene.add(backLight);
        
        // Create the Rubik's cube (27 cubies in 3x3x3 grid)
        this.createCube();
        
        // Controls
        this.setupControls();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
        
        // Start animation loop
        this.animate();
        
        // Start autonomous behavior
        if (this.autonomousMode) {
            this.startAutonomousBehavior();
        }
    }
    
    createCube() {
        this.cube = new THREE.Group();
        this.cubies = [];
        
        let cubieId = 0;
        
        // Create 3x3x3 grid of cubies
        for (let x = -1; x <= 1; x++) {
            for (let y = -1; y <= 1; y++) {
                for (let z = -1; z <= 1; z++) {
                    const cubie = this.createCubie(
                        x * this.cubeSpacing,
                        y * this.cubeSpacing,
                        z * this.cubeSpacing,
                        cubieId
                    );
                    
                    this.cube.add(cubie);
                    this.cubies.push({
                        mesh: cubie,
                        id: cubieId,
                        position: { x, y, z },
                        role: this.getCubieRole(cubieId),
                        active: false,
                        energy: 0,
                        development: 0
                    });
                    
                    cubieId++;
                }
            }
        }
        
        this.scene.add(this.cube);
    }
    
    createCubie(x, y, z, id) {
        const geometry = new THREE.BoxGeometry(this.cubieSize, this.cubieSize, this.cubieSize);
        
        // Create different colored faces
        const materials = [
            new THREE.MeshStandardMaterial({ color: 0x2196F3, metalness: 0.3, roughness: 0.4 }), // Right - Blue
            new THREE.MeshStandardMaterial({ color: 0x4CAF50, metalness: 0.3, roughness: 0.4 }), // Left - Green  
            new THREE.MeshStandardMaterial({ color: 0xFFFFFF, metalness: 0.3, roughness: 0.4 }), // Top - White
            new THREE.MeshStandardMaterial({ color: 0xFFEB3B, metalness: 0.3, roughness: 0.4 }), // Bottom - Yellow
            new THREE.MeshStandardMaterial({ color: 0xF44336, metalness: 0.3, roughness: 0.4 }), // Front - Red
            new THREE.MeshStandardMaterial({ color: 0xFF9800, metalness: 0.3, roughness: 0.4 })  // Back - Orange
        ];
        
        const cubie = new THREE.Mesh(geometry, materials);
        cubie.position.set(x, y, z);
        
        // Add edge lines for definition
        const edges = new THREE.EdgesGeometry(geometry);
        const lineMaterial = new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 2 });
        const wireframe = new THREE.LineSegments(edges, lineMaterial);
        cubie.add(wireframe);
        
        // Store cubie ID for interaction
        cubie.userData = { id, x, y, z };
        
        return cubie;
    }
    
    getCubieRole(id) {
        const roles = {
            // Bottom layer (0-8): Input
            4: 'perception_center',
            0: 'text_input', 1: 'pattern_input', 2: 'sequence_input',
            3: 'numeric_input', 5: 'binary_input', 6: 'composite_input',
            7: 'signal_routing', 8: 'input_buffer',
            
            // Middle layer (9-17): Processing
            13: 'executive_center',
            9: 'reactive', 10: 'pattern_matching', 11: 'tool_use',
            12: 'emotional', 14: 'code_synthesis', 15: 'pattern_storage',
            16: 'decision_routing', 17: 'intention_eval',
            
            // Top layer (18-26): Output
            22: 'integration_center',
            18: 'synthesis_buffer', 19: 'coherence_eval', 20: 'introspection',
            21: 'output_routing', 23: 'response_synthesis', 24: 'amplification',
            25: 'reflection', 26: 'manifestation'
        };
        return roles[id] || 'processing';
    }
    
    setupControls() {
        // Orbital controls for user to rotate view
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.minDistance = 5;
        this.controls.maxDistance = 20;
        
        // Raycaster for click detection
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        
        this.renderer.domElement.addEventListener('click', (event) => {
            this.onCubieClick(event);
        });
        
        this.renderer.domElement.addEventListener('mousemove', (event) => {
            this.onCubieHover(event);
        });
    }
    
    onCubieClick(event) {
        const rect = this.renderer.domElement.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        
        this.raycaster.setFromCamera(this.mouse, this.camera);
        
        // Check intersections with all cubie meshes
        const cubieMeshes = this.cubies.map(c => c.mesh);
        const intersects = this.raycaster.intersectObjects(cubieMeshes, true);
        
        if (intersects.length > 0) {
            // Find which cubie was clicked
            const clickedMesh = intersects[0].object.parent || intersects[0].object;
            const cubie = this.cubies.find(c => c.mesh === clickedMesh);
            
            if (cubie) {
                this.showCubieDetails(cubie.id);
            }
        }
    }
    
    onCubieHover(event) {
        const rect = this.renderer.domElement.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        
        this.raycaster.setFromCamera(this.mouse, this.camera);
        
        // Reset all cubies to normal scale first
        this.cubies.forEach(c => {
            if (!c.active) {
                c.mesh.scale.set(1, 1, 1);
            }
        });
        
        // Check intersections
        const cubieMeshes = this.cubies.map(c => c.mesh);
        const intersects = this.raycaster.intersectObjects(cubieMeshes, true);
        
        if (intersects.length > 0) {
            const hoveredMesh = intersects[0].object.parent || intersects[0].object;
            const cubie = this.cubies.find(c => c.mesh === hoveredMesh);
            
            if (cubie && !cubie.active) {
                // Slightly enlarge hovered cubie
                cubie.mesh.scale.set(1.1, 1.1, 1.1);
            }
            this.renderer.domElement.style.cursor = 'pointer';
        } else {
            this.renderer.domElement.style.cursor = 'default';
        }
    }
    
    showCubieDetails(cubieId) {
        const cubie = this.cubies[cubieId];
        if (!cubie) return;
        
        // Emit event for UI to show details panel
        const event = new CustomEvent('cubieClicked', {
            detail: {
                id: cubieId,
                role: cubie.role,
                position: cubie.position,
                energy: cubie.energy,
                development: cubie.development,
                active: cubie.active
            }
        });
        document.dispatchEvent(event);
    }
    
    activateCubies(cubieIds, energy = 0.8, duration = 300) {
        cubieIds.forEach(id => {
            if (id < this.cubies.length) {
                const cubie = this.cubies[id];
                cubie.active = true;
                cubie.energy = energy;
                
                // Visual feedback - glow effect
                cubie.mesh.material.forEach(mat => {
                    if (mat.emissive) {
                        mat.emissive.setHex(0x64b5f6);
                        mat.emissiveIntensity = energy;
                    }
                });
                
                // Scale pulse
                cubie.mesh.scale.set(1.2, 1.2, 1.2);
                
                // Reset after duration
                setTimeout(() => {
                    cubie.active = false;
                    cubie.mesh.scale.set(1, 1, 1);
                    cubie.mesh.material.forEach(mat => {
                        if (mat.emissive) {
                            mat.emissiveIntensity = 0;
                        }
                    });
                }, duration);
            }
        });
    }
    
    async executeMove(moveData) {
        return new Promise((resolve) => {
            const { move, cubies_affected, duration, energy, description } = moveData;
            
            // Show processing label
            this.updateLabel(description || move);
            
            // Activate affected cubies
            this.activateCubies(cubies_affected, energy, duration);
            
            // Perform cube rotation animation
            this.rotateFace(move, duration / 1000).then(() => {
                resolve();
            });
        });
    }
    
    async rotateFace(move, duration = 0.3) {
        return new Promise((resolve) => {
            const face = move[0];
            const isPrime = move.includes("'");
            const angle = isPrime ? -Math.PI / 2 : Math.PI / 2;
            
            // Get axis and direction based on face
            let axis = new THREE.Vector3();
            let axisDirection = 1;
            
            switch(face) {
                case 'F': axis.set(0, 0, 1); break;
                case 'B': axis.set(0, 0, -1); break;
                case 'U': axis.set(0, 1, 0); break;
                case 'D': axis.set(0, -1, 0); break;
                case 'R': axis.set(1, 0, 0); break;
                case 'L': axis.set(-1, 0, 0); break;
            }
            
            // Get cubies that need to rotate
            const affectedCubies = this.getCubiesOnFace(face);
            
            // Store original positions
            const originalPositions = affectedCubies.map(c => ({
                cubie: c,
                pos: c.mesh.position.clone()
            }));
            
            // Animate rotation
            const startTime = Date.now();
            const animate = () => {
                const elapsed = (Date.now() - startTime) / 1000;
                const progress = Math.min(elapsed / duration, 1);
                const eased = this.easeInOutCubic(progress);
                const currentAngle = angle * eased;
                
                // Apply rotation to each cubie around the axis
                affectedCubies.forEach((cubie, idx) => {
                    const original = originalPositions[idx].pos;
                    
                    // Rotate position around axis
                    const rotatedPos = original.clone();
                    rotatedPos.applyAxisAngle(axis, currentAngle);
                    cubie.mesh.position.copy(rotatedPos);
                    
                    // Rotate the cubie mesh itself
                    cubie.mesh.rotation.x = 0;
                    cubie.mesh.rotation.y = 0;
                    cubie.mesh.rotation.z = 0;
                    
                    if (face === 'U' || face === 'D') {
                        cubie.mesh.rotation.y = currentAngle * (face === 'U' ? 1 : -1);
                    } else if (face === 'R' || face === 'L') {
                        cubie.mesh.rotation.x = currentAngle * (face === 'R' ? 1 : -1);
                    } else if (face === 'F' || face === 'B') {
                        cubie.mesh.rotation.z = currentAngle * (face === 'F' ? 1 : -1);
                    }
                });
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    // Update cubie logical positions after rotation
                    affectedCubies.forEach(cubie => {
                        // Round to nearest grid position
                        cubie.position.x = Math.round(cubie.mesh.position.x);
                        cubie.position.y = Math.round(cubie.mesh.position.y);
                        cubie.position.z = Math.round(cubie.mesh.position.z);
                        
                        // Snap mesh to grid
                        cubie.mesh.position.set(
                            cubie.position.x * this.cubeSpacing,
                            cubie.position.y * this.cubeSpacing,
                            cubie.position.z * this.cubeSpacing
                        );
                        
                        // Reset rotation (already applied to materials)
                        cubie.mesh.rotation.set(0, 0, 0);
                    });
                    resolve();
                }
            };
            animate();
        });
    }
    
    getCubiesOnFace(face) {
        // Return cubies that belong to each face
        const faceMap = {
            'F': this.cubies.filter(c => c.position.z === 1),   // Front
            'B': this.cubies.filter(c => c.position.z === -1),  // Back
            'U': this.cubies.filter(c => c.position.y === 1),   // Up
            'D': this.cubies.filter(c => c.position.y === -1),  // Down
            'R': this.cubies.filter(c => c.position.x === 1),   // Right
            'L': this.cubies.filter(c => c.position.x === -1)   // Left
        };
        return faceMap[face] || [];
    }
    
    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
    
    async playSequence(moves) {
        this.isAnimating = true;
        
        for (const move of moves) {
            await this.executeMove(move);
            await this.sleep(100); // Small delay between moves
        }
        
        this.isAnimating = false;
        this.updateLabel('');
        
        // Process next in queue if any
        if (this.animationQueue.length > 0) {
            const next = this.animationQueue.shift();
            this.playSequence(next);
        }
    }
    
    queueAnimation(moves) {
        if (this.isAnimating) {
            this.animationQueue.push(moves);
        } else {
            this.playSequence(moves);
        }
    }
    
    updateLabel(text) {
        const labelElement = document.getElementById('cube-status-label');
        if (labelElement) {
            labelElement.textContent = text;
            labelElement.style.opacity = text ? '1' : '0';
        }
    }
    
    startAutonomousBehavior() {
        // Autonomous thinking animation - cube moves on its own
        setInterval(() => {
            if (this.autonomousMode && !this.isAnimating && this.animationQueue.length === 0) {
                // Random autonomous behavior
                const behaviors = ['self_reflection', 'exploration', 'optimization'];
                const behavior = behaviors[Math.floor(Math.random() * behaviors.length)];
                
                // This would be replaced with real autonomous animations from backend
                // For now, just do a subtle rotation
                this.playSubtleAutonomousAnimation();
            }
        }, 10000); // Every 10 seconds
    }
    
    async playSubtleAutonomousAnimation() {
        const autonomousMoves = [
            { move: 'U', description: '🤔 Autonomous reflection...', duration: 800, cubies_affected: [18, 19, 20, 21, 22, 23, 24, 25, 26], energy: 0.5 }
        ];
        await this.playSequence(autonomousMoves);
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Gentle cube rotation when idle
        if (!this.isAnimating) {
            this.cube.rotation.y += 0.001;
        }
        
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    _initializeState() {
        return {
            rotations: [],
            currentArrangement: 'solved'
        };
    }
    
    setAutonomousMode(enabled) {
        this.autonomousMode = enabled;
    }
}

// Export for use in main script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RubiksCube;
}
