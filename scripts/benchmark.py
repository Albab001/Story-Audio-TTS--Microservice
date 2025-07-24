#!/usr/bin/env python3
"""
Benchmark script for Story2Audio service.

Measures performance metrics for audio generation.
"""
import asyncio
import time
import statistics
from typing import List
from api.grpc_client import Story2AudioClient


async def benchmark_request(client: Story2AudioClient, story_text: str) -> dict:
    """Benchmark a single request."""
    start_time = time.time()
    try:
        audio_base64, status, message = await client.generate_audio(story_text, timeout=300)
        duration = time.time() - start_time
        
        return {
            "duration": duration,
            "status": status,
            "success": status == "success",
            "audio_size": len(audio_base64) if audio_base64 else 0,
            "error": message if status != "success" else None
        }
    except Exception as e:
        return {
            "duration": time.time() - start_time,
            "status": "error",
            "success": False,
            "audio_size": 0,
            "error": str(e)
        }


async def run_benchmark(
    num_requests: int = 10,
    story_text: str = None,
    host: str = "localhost",
    port: int = 50051
):
    """Run benchmark tests."""
    if story_text is None:
        story_text = "Once upon a time, in a magical forest, there lived a wise old owl. " * 10
    
    client = Story2AudioClient(host=host, port=port)
    
    print(f"Running benchmark: {num_requests} requests")
    print(f"Story length: {len(story_text.split())} words")
    print("-" * 50)
    
    results: List[dict] = []
    
    for i in range(num_requests):
        print(f"Request {i+1}/{num_requests}...", end=" ", flush=True)
        result = await benchmark_request(client, story_text)
        results.append(result)
        
        if result["success"]:
            print(f"✓ {result['duration']:.2f}s")
        else:
            print(f"✗ {result['error']}")
    
    # Calculate statistics
    successful = [r for r in results if r["success"]]
    
    if successful:
        durations = [r["duration"] for r in successful]
        audio_sizes = [r["audio_size"] for r in successful]
        
        print("\n" + "=" * 50)
        print("Benchmark Results")
        print("=" * 50)
        print(f"Total requests: {num_requests}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {num_requests - len(successful)}")
        print(f"Success rate: {len(successful)/num_requests*100:.1f}%")
        print(f"\nDuration Statistics:")
        print(f"  Min: {min(durations):.2f}s")
        print(f"  Max: {max(durations):.2f}s")
        print(f"  Mean: {statistics.mean(durations):.2f}s")
        print(f"  Median: {statistics.median(durations):.2f}s")
        print(f"  Std Dev: {statistics.stdev(durations):.2f}s")
        print(f"\nAudio Size Statistics:")
        print(f"  Mean: {statistics.mean(audio_sizes)/1024:.2f} KB")
        print(f"  Min: {min(audio_sizes)/1024:.2f} KB")
        print(f"  Max: {max(audio_sizes)/1024:.2f} KB")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Benchmark Story2Audio service")
    parser.add_argument("-n", "--num-requests", type=int, default=10, help="Number of requests")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    parser.add_argument("--story", help="Custom story text")
    
    args = parser.parse_args()
    
    asyncio.run(run_benchmark(
        num_requests=args.num_requests,
        story_text=args.story,
        host=args.host,
        port=args.port
    ))
