<script lang="ts">
	export let className = 'w-8 h-8';
</script>

<div class="{className} relative flex items-center justify-center">
	<svg
		viewBox="0 0 200 200"
		fill="none"
		xmlns="http://www.w3.org/2000/svg"
		class="w-full h-full drop-shadow-lg"
	>
		<defs>
			<linearGradient id="zenith-grad" x1="0%" y1="0%" x2="100%" y2="100%">
				<stop offset="0%" stop-color="#8B5CF6" />
				<stop offset="100%" stop-color="#3B82F6" />
			</linearGradient>
			<filter id="zenith-glow" x="-20%" y="-20%" width="140%" height="140%">
				<feGaussianBlur stdDeviation="5" result="blur" />
				<feComposite in="SourceGraphic" in2="blur" operator="over" />
			</filter>
		</defs>
		<!-- Futuristic 'A' shape with Zenith theme -->
		<path
			d="M100 20L40 160H65L100 70L135 160H160L100 20Z"
			fill="url(#zenith-grad)"
			filter="url(#zenith-glow)"
		/>
		<!-- Anti-gravity Orbit / Zenith Ring -->
		<ellipse cx="100" cy="110" rx="70" ry="15" stroke="white" stroke-width="2" stroke-opacity="0.3" fill="none" transform="rotate(-15 100 110)" />
		<circle cx="45" cy="110" r="4" fill="#8B5CF6" filter="url(#zenith-glow)">
			<animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite" />
		</circle>
	</svg>
</div>
